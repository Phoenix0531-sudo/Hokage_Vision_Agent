from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "apps" / "desktop" / "main.py"
DIST_DIR = ROOT / "dist" / "desktop"
BUILD_DIR = ROOT / "build" / "pyinstaller"


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--name",
            "hokage-vision-agent",
            "--noconfirm",
            "--clean",
            "--distpath",
            str(DIST_DIR),
            "--workpath",
            str(BUILD_DIR),
            "--specpath",
            str(BUILD_DIR),
            "--paths",
            str(ROOT / "src"),
            "--exclude-module",
            "torch",
            "--exclude-module",
            "ultralytics",
            str(ENTRYPOINT),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
