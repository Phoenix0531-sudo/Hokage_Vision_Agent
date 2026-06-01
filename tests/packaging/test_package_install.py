from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _venv_python(venv: Path) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def _venv_console(venv: Path, name: str) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / f"{name}.exe"
    return venv / "bin" / name


def test_wheel_build_and_console_script(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    venv_dir = tmp_path / "venv"

    subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--outdir", str(dist_dir)],
        check=True,
    )

    wheels = sorted(dist_dir.glob("*.whl"))
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    assert wheels
    assert sdists

    subprocess.run(
        [sys.executable, "-m", "venv", "--system-site-packages", str(venv_dir)], check=True
    )
    subprocess.run(
        [_venv_python(venv_dir), "-m", "pip", "install", "--no-deps", str(wheels[0])],
        check=True,
    )

    result = subprocess.run(
        [_venv_console(venv_dir, "hokage-vision"), "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Hokage Vision Agent command line interface" in result.stdout
