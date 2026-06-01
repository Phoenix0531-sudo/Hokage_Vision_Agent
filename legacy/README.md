# Legacy Project

This directory is reserved for the original YOLOv5 + PySide6 project files during the migration to Hokage Vision Agent.

The legacy code is preserved for compatibility, auditability, and migration reference. It must not be imported directly into the new `src/hokage_vision` package except through an explicit legacy backend boundary.

Known legacy concerns:

- Root-level YOLOv5 code is likely governed by upstream YOLOv5 licensing.
- The old GUI hardcodes a local Anaconda Qt plugin path.
- The old GUI hardcodes `runs/train/exp/weights/best.pt`.
- Dataset and model provenance is not fully documented.

Future phases should move the old root-level project into `legacy/old_project/` after the new mock-first project skeleton is runnable.
