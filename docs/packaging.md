# Packaging

Hokage Vision Agent is packaged as a standard Python project with `pyproject.toml` and the `hokage-vision` console script.

Build the source distribution and wheel:

```bash
docker compose run --rm package python -m build
```

Or run the wrapper:

```bash
python scripts/build_package.py
```

The package build does not bundle model weights, datasets, API keys, or desktop executables. Those artifacts are managed separately.
