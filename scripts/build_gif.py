"""Build animated GIF from captured frames."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FRAMES_DIR = ROOT / "docs" / "assets" / "frames"
OUTPUT = ROOT / "docs" / "assets" / "demo.gif"
HERO = ROOT / "docs" / "assets" / "hero.png"
REPORT = ROOT / "docs" / "assets" / "report.png"


def load_resized(path: Path, width: int = 1280) -> Image.Image:
    image = Image.open(path).convert("RGB")
    ratio = width / image.width
    height = int(image.height * ratio)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    sequence: list[Image.Image] = []

    if HERO.exists():
        sequence.append(load_resized(HERO))
        sequence.append(load_resized(HERO))

    frame_paths = sorted(FRAMES_DIR.glob("*.png"))
    for path in frame_paths:
        sequence.append(load_resized(path))

    if REPORT.exists():
        sequence.append(load_resized(REPORT))
        sequence.append(load_resized(REPORT))

    if not sequence:
        raise SystemExit("No frames found. Run scripts/capture_assets.py first.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sequence[0].save(
        OUTPUT,
        save_all=True,
        append_images=sequence[1:],
        duration=700,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT} ({len(sequence)} frames)")


if __name__ == "__main__":
    main()
