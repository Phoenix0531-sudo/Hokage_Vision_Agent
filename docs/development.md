# Development And Release

## Docker First

Docker is the main entry point for development, testing, API serving, documentation builds, package builds, and desktop build smoke checks.

```bash
docker compose build
docker compose run --rm test
docker compose run --rm gui-test
docker compose up api
docker compose run --rm docs
docker compose run --rm package
docker compose run --rm desktop-build
```

The Dockerfile uses `python:3.12-slim-bookworm` and keeps dependency layers separate from source code layers. BuildKit cache mounts are used for apt and pip caches.

If the default Debian mirror is unstable:

```bash
DEBIAN_MIRROR=http://mirrors.ustc.edu.cn/debian \
DEBIAN_SECURITY_MIRROR=http://mirrors.ustc.edu.cn/debian-security \
docker compose build gui-test
```

Headless GUI tests run with `QT_QPA_PLATFORM=offscreen`. Docker is not advertised as a zero-configuration way to display a real desktop GUI on every host OS.

## Local Optional

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
```

## Python Package

```bash
docker compose run --rm package python -m build
```

The package build does not bundle model weights, datasets, API keys, or desktop executables.

## Desktop Executable

```bash
docker compose run --rm desktop-build
```

The PyInstaller build currently targets Linux. Windows and macOS are best-effort CI targets. Model weights stay external and are configured at runtime.

## Contribution Rules

Run Ruff, unit/integration tests, and GUI tests when touching PySide6 code. Do not commit generated runs, model weights, private datasets, API keys, or raw copyrighted images. Data and model contributions must include provenance, license, class list, and redistribution information.
