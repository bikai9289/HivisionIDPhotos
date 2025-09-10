import os
import sys
import subprocess
from pathlib import Path


"""
Ensure required model weights exist before starting the app.

Behavior:
- By default, ensures lightweight CPU-friendly models are present:
  - hivision_modnet
  - modnet_photographic_portrait_matting
- If env DOWNLOAD_ALL_MODELS=true or WEIGHTS_MODELS=all, downloads all models.
- You can customize with env WEIGHTS_MODELS (space separated):
  e.g. WEIGHTS_MODELS="hivision_modnet modnet_photographic_portrait_matting retinaface-resnet50"

This script is idempotent: it only downloads missing files.
"""


BASE_DIR = Path(__file__).resolve().parent.parent
WEIGHTS_DIR = BASE_DIR / "hivision" / "creator" / "weights"
RETINAFACE_WEIGHTS_DIR = BASE_DIR / "hivision" / "creator" / "retinaface" / "weights"


def have_weight(model: str) -> bool:
    """Check if the target model seems to exist based on expected filenames."""
    if model == "retinaface-resnet50":
        file = RETINAFACE_WEIGHTS_DIR / "retinaface-resnet50.onnx"
        return file.exists() and file.stat().st_size > 1024 * 1024
    # default weights live under WEIGHTS_DIR
    patterns = {
        "hivision_modnet": "hivision_modnet.onnx",
        "modnet_photographic_portrait_matting": "modnet_photographic_portrait_matting.onnx",
        "rmbg-1.4": "rmbg-1.4.onnx",
        "birefnet-v1-lite": "birefnet-v1-lite.onnx",
    }
    fname = patterns.get(model)
    if not fname:
        # Unknown model: best-effort presence check by stem
        stem = model
        for p in WEIGHTS_DIR.glob("*.onnx"):
            if p.stem == stem and p.stat().st_size > 1024 * 100:  # >100KB
                return True
        return False
    file = WEIGHTS_DIR / fname
    return file.exists() and file.stat().st_size > 1024 * 100


def run_download(models: list[str]) -> int:
    if not models:
        return 0
    print(f"[ensure_weights] downloading missing models: {models}")
    cmd = [sys.executable, str(BASE_DIR / "scripts" / "download_model.py"), "--models", *models]
    return subprocess.call(cmd)


def main() -> int:
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    RETINAFACE_WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

    download_all = str(os.environ.get("DOWNLOAD_ALL_MODELS", "false")).lower() in (
        "1",
        "true",
        "yes",
    )
    weights_env = os.environ.get("WEIGHTS_MODELS", "").strip()

    if download_all or weights_env.lower() == "all":
        targets = ["all"]
    elif weights_env:
        targets = [m for m in weights_env.split() if m]
    else:
        # default minimal set for CPU-only servers
        targets = [
            "hivision_modnet",
            "modnet_photographic_portrait_matting",
        ]

    if targets == ["all"]:
        # Let download script handle the list
        return run_download(targets)

    # Filter to missing ones
    missing = [m for m in targets if not have_weight(m)]
    if not missing:
        print("[ensure_weights] all required weights already present.")
        return 0
    return run_download(missing)


if __name__ == "__main__":
    raise SystemExit(main())

