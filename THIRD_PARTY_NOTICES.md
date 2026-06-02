# Third-Party Notices

This file records third-party components and license boundaries for Hokage Vision Agent.

## Legacy YOLOv5 Code

The repository contains upstream-like YOLOv5 code isolated under `legacy/old_project/`, including training, validation, export, model, utility, classification, and segmentation modules. Best-effort comparison indicates the retained snapshot is closest to Ultralytics YOLOv5 `v7.0`, with several core files matching exactly. Local evidence points to a GPL-3.0-era YOLOv5 import, while current upstream YOLOv5 uses AGPL-3.0. Until provenance is fully confirmed, this code is treated as legacy YOLOv5 code governed by the applicable upstream YOLOv5 license for the imported version.

The new `src/hokage_vision` package must not copy or mix this code directly.

## Python Dependencies

Planned runtime and development dependencies include PySide6, FastAPI, Uvicorn, Pydantic, PyYAML, Typer, Rich, Pillow, NumPy, OpenCV, pytest, pytest-qt, Ruff, MkDocs, PyInstaller, Ultralytics, and optional OpenAI/LangGraph integrations. Dependency licenses must be reviewed before a formal release.

## Model Weights

Model weights are not part of the main source license. Historical Hokage/Naruto weights are treated as research and portfolio artifacts only, non-commercial, and not redistributed until the training data and model provenance are documented. Future release weights must include separate provenance and license information before distribution.

## Dataset Images and Annotations

Dataset images are not redistributed unless rights are verified. User-provided or locally captured anime screenshots are treated as local research material only. Dataset annotations require a separate licensing decision after the source image rights are reviewed.

## Legacy Binary Artifacts

The old project previously depended on local Qt/OpenGL binary runtime files. The undocumented legacy `libEGL.dll` has been removed from the current tree and is not redistributed.

## Documentation

Project documentation may be licensed separately, for example under CC BY 4.0, if the maintainers choose to do so.

## Docker and CI

Docker images use official Python base images and Debian packages. GitHub Actions workflows use third-party actions such as `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, GitHub Pages deployment actions, CodeQL actions, and release artifact actions. These remain under their own licenses and terms.
