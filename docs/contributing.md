# Contributing

Use Docker first:

```bash
docker compose build
docker compose run --rm test
docker compose run --rm gui-test
```

Recommended local developer setup:

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
pre-commit install
```

Before opening a pull request:

- Run Ruff formatting and lint checks.
- Run unit and integration tests.
- Run GUI tests when touching PySide6 code.
- Update docs for behavior, command, model, data, or license changes.
- Do not commit generated runs, model weights, private datasets, API keys, or raw copyrighted images.

Data and model contributions must include provenance, license, class list, and redistribution information.
