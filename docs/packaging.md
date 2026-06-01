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

## Desktop Executable

The desktop build uses PyInstaller. The current supported target is Linux; Windows and macOS are reserved in CI as best-effort targets.

```bash
docker compose run --rm desktop-build
```

The desktop executable does not bundle large model weights. Configure model paths at runtime through the GUI settings or external config files.
