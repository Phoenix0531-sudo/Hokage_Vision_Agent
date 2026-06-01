# Docker

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

The Dockerfile uses `python:3.12-slim-bookworm` and keeps dependency layers separate from source code layers. The normal `test` image does not install PySide6 or Qt system libraries. The `gui-test` image installs the headless Qt dependencies and `PySide6-Essentials` before copying source files, so changing application code should not invalidate the expensive GUI dependency layers.

API, docs, and desktop build dependencies also live in their own cached stages. The runtime commands do not install Uvicorn, MkDocs, or PyInstaller on every container start.

BuildKit cache mounts are used for apt and pip caches. If the default Debian mirror is unstable in your network, pass a mirror through environment variables:

```bash
DEBIAN_MIRROR=http://mirrors.ustc.edu.cn/debian \
DEBIAN_SECURITY_MIRROR=http://mirrors.ustc.edu.cn/debian-security \
docker compose build gui-test
```

Headless GUI tests run with `QT_QPA_PLATFORM=offscreen`. Docker is not advertised as a zero-configuration way to display a real desktop GUI on every host OS.
