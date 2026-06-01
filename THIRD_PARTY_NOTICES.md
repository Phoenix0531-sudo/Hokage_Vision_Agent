# Third-Party Notices

This file records third-party components and license boundaries for Hokage Vision Agent.

## Legacy YOLOv5 Code

The current repository contains upstream-like YOLOv5 code in the root tree, including training, validation, export, model, utility, classification, and segmentation modules. Until provenance is fully confirmed, this code is treated as legacy YOLOv5 code governed by the applicable upstream YOLOv5 license.

The new `src/hokage_vision` package must not copy or mix this code directly.

## Python Dependencies

Planned runtime and development dependencies include PySide6, FastAPI, Uvicorn, Pydantic, PyYAML, Typer, Rich, Pillow, NumPy, OpenCV, pytest, pytest-qt, Ruff, MkDocs, PyInstaller, Ultralytics, and optional OpenAI/LangGraph integrations. Dependency licenses must be reviewed before a formal release.

## Model Weights

Model weights are not part of the main source license. They must include separate provenance and license information before distribution.

## Dataset Images and Annotations

Dataset images are not redistributed unless rights are verified. Dataset annotations require a separate licensing decision after the source image rights are reviewed.

## Documentation

Project documentation may be licensed separately, for example under CC BY 4.0, if the maintainers choose to do so.
