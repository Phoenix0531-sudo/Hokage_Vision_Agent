# License Boundaries

This repository currently contains both new Hokage Vision Agent code and legacy YOLOv5-derived code. Treat license boundaries carefully until legacy migration is complete.

## Main Project Source Code

New code under `src/hokage_vision`, `apps`, `scripts`, tests, Docker files, workflows, and project documentation is intended to be Apache-2.0 unless a file states otherwise.

## Legacy YOLOv5 Code

Legacy YOLOv5-derived files remain governed by the applicable upstream YOLOv5 license for the imported version. Best-effort comparison indicates the retained snapshot is closest to Ultralytics YOLOv5 `v7.0`, with several core files matching exactly, but the original import tag was not recorded. Do not copy legacy YOLOv5 code into `src/hokage_vision`.

## Documentation

Documentation is maintained with the project. A separate CC BY 4.0 declaration can be added later if maintainers choose to split documentation licensing from source code.

## Model Weights

Model weights are separately licensed artifacts. They must include provenance, classes, training data summary, metrics, and license before distribution. Current policy for historical Hokage/Naruto weights is research and portfolio use only, non-commercial, and not redistributed until provenance is documented. Large weights must not be committed to git.

## Datasets and Annotations

Dataset images are not redistributed unless rights are verified. User-provided or locally captured anime screenshots are treated as local research material, not public reusable data. Annotation files can only be licensed after the associated image rights and redistribution terms are reviewed.

## Legacy Binary Artifacts

The old project previously depended on local Qt/OpenGL binary runtime files. Undocumented binary artifacts such as the legacy `libEGL.dll` are not redistributed in the current tree.

## Third-Party Dependencies

Python dependencies, Docker base images, GitHub Actions, PySide6/Qt libraries, and optional LLM integrations remain under their own licenses. See `THIRD_PARTY_NOTICES.md`.
