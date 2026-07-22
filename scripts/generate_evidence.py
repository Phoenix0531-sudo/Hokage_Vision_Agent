"""Generate portfolio evidence: mock backend boxes on a synthetic image + architecture card."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hokage_vision.vision.backends.mock import MockBackend

OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
FIXTURES = ROOT / "docs" / "screenshots" / "fixtures"
FIXTURES.mkdir(parents=True, exist_ok=True)

BG = "#0b1220"
PANEL = "#111827"
FG = "#e5e7eb"
ACCENT = "#38bdf8"
GOOD = "#34d399"
MUTED = "#94a3b8"
BOX_COLORS = ["#f472b6", "#38bdf8", "#fbbf24"]


def make_demo_image(path: Path, w: int = 640, h: int = 400) -> Path:
    img = Image.new("RGB", (w, h), (18, 24, 38))
    draw = ImageDraw.Draw(img)
    # abstract character-like silhouettes (not claiming real anime assets)
    for i, cx in enumerate((140, 320, 500)):
        color = [(244, 114, 182), (56, 189, 248), (251, 191, 36)][i]
        draw.ellipse((cx - 40, 90, cx + 40, 170), fill=color)
        draw.rectangle((cx - 35, 170, cx + 35, 300), fill=tuple(int(c * 0.7) for c in color))
    draw.text((16, 12), "demo fixture (not licensed artwork)", fill=(148, 163, 184))
    img.save(path)
    return path


def main() -> None:
    fixture = make_demo_image(FIXTURES / "demo_scene.png")
    backend = MockBackend()
    backend.load()
    result = backend.predict_image(fixture)

    fig = plt.figure(figsize=(12.8, 7.2), facecolor=BG)
    gs = GridSpec(2, 3, figure=fig, wspace=0.25, hspace=0.3, left=0.05, right=0.98, top=0.88, bottom=0.08)

    ax_img = fig.add_subplot(gs[:, 0:2])
    ax_img.set_facecolor(PANEL)
    ax_img.set_title("MockBackend.predict_image — deterministic boxes", color=FG, fontsize=11)
    arr = np.array(Image.open(fixture))
    ax_img.imshow(arr)
    for i, det in enumerate(result.detections):
        x1, y1, x2, y2 = det.box.x1, det.box.y1, det.box.x2, det.box.y2
        # BoundingBox fields may be named differently — support both
        if hasattr(det.box, "x_min"):
            x1, y1, x2, y2 = det.box.x_min, det.box.y_min, det.box.x_max, det.box.y_max
        w, h = x2 - x1, y2 - y1
        color = BOX_COLORS[i % len(BOX_COLORS)]
        ax_img.add_patch(Rectangle((x1, y1), w, h, fill=False, edgecolor=color, lw=2.2))
        ax_img.text(
            x1,
            max(0, y1 - 6),
            f"{det.label} {det.confidence:.2f}",
            color=color,
            fontsize=9,
            fontweight="bold",
            va="bottom",
        )
    ax_img.set_xticks([])
    ax_img.set_yticks([])
    for s in ax_img.spines.values():
        s.set_color("#1f2937")

    ax_card = fig.add_subplot(gs[0, 2])
    ax_card.set_facecolor(PANEL)
    ax_card.axis("off")
    lines = [
        "DETECTION EVIDENCE",
        f"backend   = {result.metadata.get('backend')}",
        f"size      = {result.width}x{result.height}",
        f"count     = {len(result.detections)}",
    ]
    for det in result.detections:
        lines.append(f"- {det.label}: {det.confidence:.2f}")
    lines += [
        "",
        "Agent never invents boxes;",
        "tools call InferenceService only.",
    ]
    ax_card.text(0.05, 0.95, "\n".join(lines), transform=ax_card.transAxes, va="top", color=FG, family="monospace", fontsize=9)

    ax_arch = fig.add_subplot(gs[1, 2])
    ax_arch.set_facecolor(PANEL)
    ax_arch.axis("off")
    ax_arch.text(
        0.05,
        0.95,
        "\n".join(
            [
                "SURFACES",
                "CLI  hokage-vision",
                "API  FastAPI",
                "GUI  PySide6",
                "Agent tool registry",
                "",
                "BACKENDS",
                "mock | ultralytics | yolov5-legacy",
                "",
                "CI: unit + integration",
                "default mock (no GPU)",
            ]
        ),
        transform=ax_arch.transAxes,
        va="top",
        color=FG,
        family="monospace",
        fontsize=9,
    )

    fig.suptitle(
        "Hokage Vision Agent — mock-backend evidence (reproducible, no private weights)",
        color=FG,
        fontsize=13,
        fontweight="bold",
        y=0.96,
    )
    out = OUT / "evidence.png"
    fig.savefig(out, dpi=160, facecolor=BG)
    plt.close(fig)
    print(f"wrote {out} detections={len(result.detections)}")


if __name__ == "__main__":
    main()
