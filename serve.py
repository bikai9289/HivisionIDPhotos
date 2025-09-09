import os
import pathlib
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response, RedirectResponse
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

    # Static (site styles)
    static_dir = base_dir / "web" / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    # Public demo assets (images) — use a non-conflicting path since Gradio also serves 
    # its frontend bundles at "/assets". We choose "/site-assets" for site images.
    assets_dir = base_dir / "assets"
    if assets_dir.exists():
        app.mount("/site-assets", StaticFiles(directory=str(assets_dir)), name="site-assets")

    # Home: default to English, keep language-specific routes
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        return RedirectResponse(url="/en")

    @app.get("/en", response_class=HTMLResponse)
    async def home_en(request: Request):
        return templates.TemplateResponse(
            "index_en.html",
            {
                "request": request,
                "now": datetime.utcnow(),
            },
        )

    # Chinese home at /zh
    @app.get("/zh", response_class=HTMLResponse)
    async def home_zh(request: Request):
        return templates.TemplateResponse(
            "index_zh.html",
            {
                "request": request,
                "now": datetime.utcnow(),
            },
        )

    # Programmatic spec pages: Chinese default
    @app.get("/spec/{slug}", response_class=HTMLResponse)
    async def spec_zh(request: Request, slug: str):
        data = spec_cn_by_slug.get(slug)
        if not data:
            return HTMLResponse("<h1>404</h1>", status_code=404)
        return templates.TemplateResponse(
            "spec.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "lang": "zh-CN",
                "data": data,
            },
        )

    # Programmatic spec pages: English
    @app.get("/en/spec/{slug}", response_class=HTMLResponse)
    async def spec_en(request: Request, slug: str):
        data = spec_en_by_slug.get(slug)
        if not data:
            return HTMLResponse("<h1>404</h1>", status_code=404)
        return templates.TemplateResponse(
            "spec.html",
            {
                "request": request,
                "now": datetime.utcnow(),
                "lang": "en",
                "data": data,
            },
        )

    # robots.txt
    @app.get("/robots.txt", response_class=PlainTextResponse)
    async def robots():
        site = os.environ.get("PUBLIC_SITE_URL", "http://localhost:8000").rstrip("/")
        content = f"""User-agent: *
Allow: /

Sitemap: {site}/sitemap.xml
"""
        return PlainTextResponse(content)

    # sitemap.xml (enhanced: i18n alternates, metadata)
    @app.get("/sitemap.xml")
    async def sitemap():
        site = os.environ.get("PUBLIC_SITE_URL", "http://localhost:8000").rstrip("/")
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # Build entries with optional alternates
        entries: list[dict] = []

        # Home pages
        entries.append(
            {
                "path": "/",
                "lastmod": today,
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
                "lastmod": today,
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
                "lastmod": today,
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
                "lastmod": today,
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
                    "lastmod": today,
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
                    "lastmod": today,
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
        lines = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:xhtml=\"http://www.w3.org/1999/xhtml\">",
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
        return Response(content=xml, media_type="application/xml")

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
