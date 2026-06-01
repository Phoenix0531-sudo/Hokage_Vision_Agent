# Migration Plan

# Hokage Vision Agent Migration

Hokage Vision Agent will replace the current root-level YOLOv5 + PySide6 layout with a modern Python package, Docker-first developer workflow, documented data governance, a safe rule-based agent layer, a FastAPI service, and a redesigned PySide6 desktop GUI.

## Current Repository Shape

The current repository is mostly a YOLOv5-style tree at the repository root:

- Upstream-like YOLOv5 entrypoints: `detect.py`, `train.py`, `val.py`, `export.py`, `benchmarks.py`, `hubconf.py`.
- Upstream-like YOLOv5 packages and configs: `models/`, `utils/`, `classify/`, `segment/`, `data/*.yaml`, `data/hyps/`, `data/scripts/`.
- Project-specific GUI code: `base_ui.py`, `main_window.py`, `main_window.ui`, `test_open_image.py`.
- Project-specific dataset labels/classes: `datasets/classes.txt`, `datasets/labels/`.
- Demo/readme assets: `readme_images.png`, `readme_images/`.

The new project must not import YOLOv5 legacy modules directly into `src/hokage_vision`. A compatibility backend may call legacy code only through an explicit boundary.

## Migration Strategy

1. Preserve old code during the first audit phase.
2. Create a new package under `src/hokage_vision` with shared types, configuration, and mock-first inference.
3. Build CLI, API, GUI, agent, dataset, training, and model-management features against the new package.
4. Move or isolate legacy YOLOv5 code under `legacy/old_project/` once the new mock workflow is runnable.
5. Keep the legacy backend optional and documented as a compatibility path, not the default runtime.
6. Keep data, model weights, generated runs, API keys, and private datasets out of git.

## Known Legacy Risks

- `base_ui.py` hardcodes `QT_QPA_PLATFORM_PLUGIN_PATH` to a local Anaconda path.
- `base_ui.py` and `hub_detect.ipynb` hardcode `runs/train/exp/weights/best.pt`.
- Legacy YOLOv5 scripts include webcam examples and download helpers; Hokage Vision Agent must not expose camera support and must not auto-download copyrighted data.
- No root `LICENSE` file was found during the initial audit.
- The repository contains dataset label files and caches, but no dataset manifest or license provenance.
- `libEGL.dll` is committed at the repository root and needs review before any packaging decision.

## Acceptance Criteria

- Legacy code remains available for reference and compatibility.
- New code lives under `src/hokage_vision`.
- The default backend is `mock`.
- CI, GUI smoke tests, API tests, and agent tests do not depend on GPU, private data, real YOLO weights, or external LLM APIs.
- Documentation clearly separates source code, legacy code, documentation, model weights, dataset images, and annotations.
