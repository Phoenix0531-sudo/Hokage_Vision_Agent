# Contributing

Thank you for helping improve Hokage Vision Agent. This project is being migrated from a legacy YOLOv5 + PySide6 repository into a Docker-first computer vision workbench.

## Development Workflow

Use Docker first:

```bash
docker compose build
docker compose run --rm test
docker compose run --rm gui-test
```

Local development is optional:

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
pre-commit install
```

## Branches and Commits

- Use focused branches such as `feat/agent-tools`, `fix/gui-smoke`, or `docs/model-registry`.
- Use Conventional Commits, for example `feat(api): add model endpoints`.
- Keep pull requests small enough to review.

## Pull Requests

Before opening a PR:

- Run Ruff formatting and lint checks.
- Run unit and integration tests.
- Run headless GUI tests if touching `src/hokage_vision/ui` or PySide6 dependencies.
- Update docs when behavior, commands, model handling, or data handling changes.
- Do not include generated `runs/`, `dist/`, model weights, private datasets, or API keys.

## Data and Model Contributions

Dataset images must include source, license, and redistribution notes. Do not contribute Naruto or anime screenshots unless rights and redistribution terms are clear.

Model weights must include provenance, classes, training data summary, evaluation metrics, and license. Large weights should be distributed through releases or external storage, not committed to git.

## License Notes

New Hokage Vision Agent source code is intended to be Apache-2.0. Legacy YOLOv5-derived code remains governed by the applicable upstream YOLOv5 license. See `docs/license-audit.md` and `LICENSES/README.md` before moving or copying legacy code.
