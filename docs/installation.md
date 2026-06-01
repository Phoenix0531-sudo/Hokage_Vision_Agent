# Installation

Docker is the primary installation path.

```bash
docker compose build
docker compose run --rm test
```

Local installation is optional for contributors who already have a suitable Python 3.12 environment:

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
```

Use the optional dependency groups only for the surface you need:

- `gui`: PySide6 desktop application and GUI tests.
- `api`: FastAPI and Uvicorn.
- `train`: Ultralytics training/evaluation wrappers.
- `docs`: MkDocs documentation site.
- `package`: Python package build tooling.
- `desktop-build`: PyInstaller executable build.

Do not commit `.venv`, model weights, private data, generated runs, or API keys.
