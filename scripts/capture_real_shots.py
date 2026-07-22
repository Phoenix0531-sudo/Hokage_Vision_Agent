"""Capture real Qt window screenshots of Hokage Vision Agent with mock detection."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
FIXTURES = OUT / "fixtures"
FIXTURES.mkdir(exist_ok=True)

from PIL import Image, ImageDraw


def make_demo_image(path: Path, w: int = 720, h: int = 420) -> Path:
    img = Image.new("RGB", (w, h), (18, 24, 38))
    draw = ImageDraw.Draw(img)
    for i, cx in enumerate((150, 360, 560)):
        color = [(244, 114, 182), (56, 189, 248), (251, 191, 36)][i]
        draw.ellipse((cx - 45, 100, cx + 45, 190), fill=color)
        draw.rectangle((cx - 40, 190, cx + 40, 320), fill=tuple(int(c * 0.65) for c in color))
        draw.text((cx - 28, 330), ["obito", "naruto", "gaara"][i], fill=(226, 232, 240))
    draw.text((16, 12), "demo fixture for mock detection", fill=(148, 163, 184))
    img.save(path)
    return path


def main() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "windows")
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import QApplication
    import time

    app = QApplication.instance() or QApplication(sys.argv)

    from hokage_vision.ui.main_window import MainWindow

    demo = make_demo_image(FIXTURES / "demo_scene.png")

    win = MainWindow(language="zh-CN", theme="dark")
    win.resize(1280, 860)
    win.show()
    app.processEvents()
    time.sleep(0.3)
    app.processEvents()

    def grab(name: str) -> Path:
        app.processEvents()
        pix: QPixmap = win.grab()
        path = OUT / name
        if not pix.save(str(path), "PNG"):
            raise RuntimeError(f"failed {path}")
        print(f"OK {path} {path.stat().st_size} bytes")
        return path

    grab("gui_home.png")

    # Image tab + detect
    win.tabs.setCurrentIndex(1)
    app.processEvents()
    panel = win.tabs.widget(1)
    panel.detect_path(demo)
    app.processEvents()
    time.sleep(0.4)
    app.processEvents()
    grab("gui_image_detect.png")

    # Agent tab
    for i in range(win.tabs.count()):
        text = win.tabs.tabText(i)
        if "Agent" in text or "助手" in text:
            win.tabs.setCurrentIndex(i)
            app.processEvents()
            time.sleep(0.2)
            grab("gui_agent_tab.png")
            break

    win.close()
    app.quit()
    print("done")


if __name__ == "__main__":
    main()
