# Legacy Project

This directory contains the original YOLOv5 + PySide6 project files after migration to Hokage Vision Agent.

The legacy code is preserved for compatibility, auditability, and migration reference. It must not be imported directly into the new `src/hokage_vision` package except through an explicit legacy backend boundary.

Known legacy concerns:

- `legacy/old_project/` contains the old YOLOv5-style root tree and the previous PySide6 GUI files.
- Legacy YOLOv5 code is likely governed by upstream YOLOv5 licensing.
- The old GUI hardcodes a local Anaconda Qt plugin path.
- The old GUI hardcodes `runs/train/exp/weights/best.pt`.
- Dataset and model provenance is not fully documented.

Do not import this code directly from the new package. Use the explicit legacy backend boundary only.
