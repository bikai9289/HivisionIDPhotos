import os
import pathlib
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


def create_marketing_app() -> FastAPI:
    app = FastAPI(title="AI IDPhotos Site")

    base_dir = pathlib.Path(__file__).parent
    templates = Jinja2Templates(directory=str(base_dir / "web" / "templates"))

    # Load programmatic spec pages (CN/EN)
    specs_dir = base_dir / "web" / "specs"
    specs_cn = []
    specs_en = []
    try:
        import json

        if (specs_dir / "specs_zh.json").exists():
            specs_cn = json.loads((specs_dir / "specs_zh.json").read_text(encoding="utf-8"))
        if (specs_dir / "specs_en.json").exists():
            specs_en = json.loads((specs_dir / "specs_en.json").read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[serve] load specs failed: {e}")

    # Build quick lookup by slug
    spec_cn_by_slug = {s.get("slug"): s for s in specs_cn if s.get("slug")}
    spec_en_by_slug = {s.get("slug"): s for s in specs_en if s.get("slug")}

    def build_language_alternates(
        en_path: str | None = None,
        zh_path: str | None = None,
        x_default: str | None = None,
    ) -> list[dict[str, str]]:
        """Build hreflang alternate entries for templates."""
        alternates: list[dict[str, str]] = []
        if en_path:
            alternates.append({"hreflang": "en", "path": en_path})
        if zh_path:
            alternates.append({"hreflang": "zh-CN", "path": zh_path})
        if x_default:
            alternates.append({"hreflang": "x-default", "path": x_default})
        return alternates

    # Static (site styles)
    static_dir = base_dir / "web" / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    # Public demo assets (images) - use a non-conflicting path since Gradio also serves 
    # its frontend bundles at "/assets". We choose "/site-assets" for site images.
    assets_dir = base_dir / "assets"
    if assets_dir.exists():
        app.mount("/site-assets", StaticFiles(directory=str(assets_dir)), name="site-assets")
    logo_dir = base_dir / "logo"
    if logo_dir.exists():
        app.mount("/logo", StaticFiles(directory=str(logo_dir)), name="logo")


    @app.api_route("/google860540df1f459afe.html", methods=["GET", "HEAD"])
    async def google_site_verification():
        """Serve Google Search Console verification file."""
        verification_file = base_dir / "google860540df1f459afe.html"
        if verification_file.exists():
            return FileResponse(str(verification_file), media_type="text/html")
        return Response(status_code=404)

    # Home: render default language directly (no redirect)
    @app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def home(request: Request):
        # DEFAULT_LANG can be en/zh/ko/ja; default to English
        default_lang = str(os.environ.get("DEFAULT_LANG", "en")).lower()
        alternates = build_language_alternates(en_path="/", zh_path="/zh", x_default="/")
        if default_lang.startswith("zh"):
            context = {
                "request": request,
                "now": datetime.utcnow(),
                "alternates": alternates,
                "canonical_path": "/zh",
            }
            template_name = "index_zh.html"
        else:
            context = {
                "request": request,
                "now": datetime.utcnow(),
                "alternates": alternates,
            }
            template_name = "index_en.html"
        return templates.TemplateResponse(template_name, context)

    @app.api_route("/en", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def home_en(request: Request):
        return templates.TemplateResponse(
            "index_en.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "alternates": build_language_alternates(en_path="/", zh_path="/zh", x_default="/"),
                "canonical_path": "/",
            },
        )

    # Chinese home at /zh
    @app.api_route("/zh", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def home_zh(request: Request):
        return templates.TemplateResponse(
            "index_zh.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "alternates": build_language_alternates(en_path="/", zh_path="/zh", x_default="/"),
                "canonical_path": "/zh",
            },
        )

    # Programmatic spec pages: Chinese default
    @app.api_route("/spec/{slug}", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def spec_zh(request: Request, slug: str):
        data = spec_cn_by_slug.get(slug)
        if not data:
            return HTMLResponse("<h1>404</h1>", status_code=404)
        has_en = slug in spec_en_by_slug
        alternates = build_language_alternates(
            en_path=f"/en/spec/{slug}" if has_en else None,
            zh_path=f"/spec/{slug}",
            x_default=f"/en/spec/{slug}" if has_en else f"/spec/{slug}",
        )
        return templates.TemplateResponse(
            "spec.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "lang": "zh-CN",
                "data": data,
                "alternates": alternates,
                "canonical_path": f"/spec/{slug}",
            },
        )

    # Programmatic spec pages: English
    @app.api_route("/en/spec/{slug}", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def spec_en(request: Request, slug: str):
        data = spec_en_by_slug.get(slug)
        if not data:
            return HTMLResponse("<h1>404</h1>", status_code=404)
        has_cn = slug in spec_cn_by_slug
        alternates = build_language_alternates(
            en_path=f"/en/spec/{slug}",
            zh_path=f"/spec/{slug}" if has_cn else None,
            x_default=f"/en/spec/{slug}",
        )
        return templates.TemplateResponse(
            "spec.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "lang": "en",
                "data": data,
                "alternates": alternates,
                "canonical_path": f"/en/spec/{slug}",
            },
        )

    # robots.txt
    @app.api_route("/robots.txt", methods=["GET", "HEAD"], response_class=PlainTextResponse)
    async def robots():
        site = os.environ.get("PUBLIC_SITE_URL", "http://localhost:8000").rstrip("/")
        content = f"""User-agent: *
Allow: /

Sitemap: {site}/sitemap.xml
"""
        return PlainTextResponse(content)

    @app.api_route("/sitemap", methods=["GET", "HEAD"], include_in_schema=False)
    async def sitemap_redirect():
        """Ensure bare /sitemap requests go to the XML payload."""
        return RedirectResponse(url="/sitemap.xml", status_code=308)

    @app.api_route("/sitemap_index.xml", methods=["GET", "HEAD"], include_in_schema=False)
    async def sitemap_index_redirect():
        """Provide a simple alias for sitemap index probes."""
        return RedirectResponse(url="/sitemap.xml", status_code=308)

    # sitemap.xml (enhanced: i18n alternates, metadata)
    @app.api_route("/sitemap.xml", methods=["GET", "HEAD"])
    async def sitemap():
        site = os.environ.get("PUBLIC_SITE_URL", "http://localhost:8000").rstrip("/")
        generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Build entries with optional alternates
        entries: list[dict] = []

        # Home pages
        entries.append(
            {
                "path": "/",
                "lastmod": generated_at,
                "changefreq": "weekly",
                "priority": "1.0",
                "alternates": [
                    {"hreflang": "en", "path": "/en"},
                    {"hreflang": "zh-CN", "path": "/zh"},
                ],
            }
        )
        entries.append(
            {
                "path": "/en",
                "lastmod": generated_at,
                "changefreq": "weekly",
                "priority": "1.0",
                "alternates": [
                    {"hreflang": "en", "path": "/en"},
                    {"hreflang": "zh-CN", "path": "/zh"},
                ],
            }
        )
        entries.append(
            {
                "path": "/zh",
                "lastmod": generated_at,
                "changefreq": "weekly",
                "priority": "1.0",
                "alternates": [
                    {"hreflang": "en", "path": "/en"},
                    {"hreflang": "zh-CN", "path": "/zh"},
                ],
            }
        )

        # Tool page (editor)
        entries.append(
            {
                "path": "/tool",
                "lastmod": generated_at,
                "changefreq": "weekly",
                "priority": "0.6",
            }
        )

        # Spec pages (CN/EN), link alternates when both exist
        cn_slugs = {s["slug"] for s in specs_cn if s.get("slug")}
        en_slugs = {s["slug"] for s in specs_en if s.get("slug")}
        all_slugs = sorted(cn_slugs.union(en_slugs))
        for slug in all_slugs:
            has_cn = slug in cn_slugs
            has_en = slug in en_slugs
            if has_cn:
                entry = {
                    "path": f"/spec/{slug}",
                    "lastmod": generated_at,
                    "changefreq": "monthly",
                    "priority": "0.7",
                }
                if has_en:
                    entry["alternates"] = [
                        {"hreflang": "zh-CN", "path": f"/spec/{slug}"},
                        {"hreflang": "en", "path": f"/en/spec/{slug}"},
                    ]
                entries.append(entry)
            if has_en:
                entry = {
                    "path": f"/en/spec/{slug}",
                    "lastmod": generated_at,
                    "changefreq": "monthly",
                    "priority": "0.7",
                }
                if has_cn:
                    entry["alternates"] = [
                        {"hreflang": "en", "path": f"/en/spec/{slug}"},
                        {"hreflang": "zh-CN", "path": f"/spec/{slug}"},
                    ]
                entries.append(entry)

        # Render XML
        namespace_pairs = [
            ("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9"),
            ("xmlns:xhtml", "http://www.w3.org/1999/xhtml"),
            ("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1"),
            ("xmlns:news", "http://www.google.com/schemas/sitemap-news/0.9"),
            ("xmlns:mobile", "http://www.google.com/schemas/sitemap-mobile/1.0"),
            ("xmlns:video", "http://www.google.com/schemas/sitemap-video/1.1"),
        ]
        namespace_attrs = " ".join(f'{key}="{value}"' for key, value in namespace_pairs)
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<urlset {namespace_attrs}>',
        ]
        for e in entries:
            lines.append("  <url>")
            lines.append(f"    <loc>{site}{e['path']}</loc>")
            if e.get("lastmod"):
                lines.append(f"    <lastmod>{e['lastmod']}</lastmod>")
            if e.get("changefreq"):
                lines.append(f"    <changefreq>{e['changefreq']}</changefreq>")
            if e.get("priority"):
                lines.append(f"    <priority>{e['priority']}</priority>")
            for alt in e.get("alternates", []) or []:
                lines.append(
                    f"    <xhtml:link rel=\"alternate\" hreflang=\"{alt['hreflang']}\" href=\"{site}{alt['path']}\" />"
                )
            lines.append("  </url>")
        lines.append("</urlset>")

        xml = "\n".join(lines)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    return app


def build_app() -> FastAPI:
    # Main FastAPI app
    app = create_marketing_app()

    # Mount existing API under /api
    try:
        from deploy_api import app as api_app  # type: ignore

        app.mount("/api", api_app)
    except Exception as e:
        # Keep site running even if API import fails
        print(f"[serve] Skip mounting /api: {e}")

    # Mount Gradio UI under /tool
    try:
        import gradio as gr
        from demo.processor import IDPhotoProcessor
        try:
            from demo.ui import create_ui  # preferred
        except Exception:
            from demo.ui2 import create_ui  # fallback lightweight UI
        from hivision.creator.choose_handler import HUMAN_MATTING_MODELS

        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Discover available human matting models
        weights_dir = os.path.join(root_dir, "hivision/creator/weights")
        existing = [
            os.path.splitext(f)[0]
            for f in os.listdir(weights_dir)
            if f.endswith(".onnx") or f.endswith(".mnn")
        ] if os.path.exists(weights_dir) else []
        human_models = [m for m in HUMAN_MATTING_MODELS if m in existing] or [
            "modnet_photographic_portrait_matting"
        ]

        # Face detection models (best effort)
        face_models = ["mtcnn"]
        if os.path.exists(
            os.path.join(
                root_dir, "hivision/creator/retinaface/weights/retinaface-resnet50.onnx"
            )
        ):
            face_models = ["face++ (联网Online API)", "mtcnn", "retinaface-resnet50"]

        processor = IDPhotoProcessor()
        blocks = create_ui(
            processor,
            root_dir,
            human_models,
            face_models,
            ["en", "zh", "ko", "ja"],
        )

        # Prefer new helper if available; otherwise try legacy builders
        mounted = False
        try:
            from gradio.routes import mount_gradio_app  # type: ignore

            mount_gradio_app(app, blocks, path="/tool")
            mounted = True
        except Exception:
            try:
                gradio_app = gr.routes.App.create_app(blocks)  # type: ignore
                app.mount("/tool", gradio_app)
                mounted = True
            except Exception:
                mounted = False

        # Final fallback: run Gradio on a side port and redirect /tool
        if not mounted:
            try:
                tool_port = int(os.environ.get("GRADIO_TOOL_PORT", "7860"))
                # prevent_thread_lock makes it non-blocking
                blocks.queue().launch(
                    server_name="0.0.0.0",
                    server_port=tool_port,
                    share=False,
                    inbrowser=False,
                    prevent_thread_lock=True,
                )

                @app.get("/tool")
                async def tool_redirect(request: Request):  # type: ignore
                    # Preserve current hostname, swap to the Gradio side-port
                    host = request.headers.get("host", "127.0.0.1").split(":")[0]
                    scheme = "https" if request.url.scheme == "https" else "http"
                    return RedirectResponse(url=f"{scheme}://{host}:{tool_port}")

                print("[serve] Mounted /tool via redirect to side-port", tool_port)
            except Exception as e:
                print(f"[serve] Skip mounting /tool: {e}")
    except Exception as e:
        print(f"[serve] Skip preparing gradio UI: {e}")

    # Compatibility shim for Gradio file endpoint when mounted under "/tool".
    # Some Gradio frontends may still request files at root path like
    #   GET /file=/tmp/xxx.png
    # when the app is mounted at /tool. Provide a redirect so these requests
    # are forwarded to the mounted path.
    @app.get("/file={file_path:path}")
    async def _redirect_gradio_file(file_path: str):  # type: ignore
        return RedirectResponse(url=f"/tool/file={file_path}")

    # Redirect any bare gradio_api calls to the mounted path under /tool
    @app.api_route("/gradio_api/{rest:path}", methods=["GET", "POST"])  # type: ignore
    async def _redirect_gradio_api(rest: str, request: Request):
        # Preserve query string
        qs = ("?" + request.url.query) if request.url.query else ""
        return RedirectResponse(url=f"/tool/gradio_api/{rest}{qs}")

    # Minimal PWA manifest to avoid console 404 noise
    @app.api_route("/manifest.json", methods=["GET", "HEAD"])
    async def _manifest():
        return Response(
            content=(
                '{"name":"AI IDPhotos","short_name":"IDPhotos","start_url":"/tool/","display":"standalone","icons":[]}'
            ),
            media_type="application/json",
        )

    # Quiet 404 for favicon
    @app.api_route("/favicon.ico", methods=["GET", "HEAD"])
    async def _favicon():
        return Response(status_code=204)

    return app


app = build_app()


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    # Fast dev reload: flag or env RELOAD=1
    reload_flag = args.reload or (str(os.environ.get("RELOAD", "0")).lower() in ("1", "true", "yes"))
    if reload_flag:
        uvicorn.run(
            "serve:app", host=args.host, port=args.port, reload=True, reload_dirs=[os.path.dirname(__file__)]
        )
    else:
        uvicorn.run(app, host=args.host, port=args.port)

