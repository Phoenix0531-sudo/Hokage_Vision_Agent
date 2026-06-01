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

Headless GUI tests run with `QT_QPA_PLATFORM=offscreen`. Docker is not advertised as a zero-configuration way to display a real desktop GUI on every host OS.
