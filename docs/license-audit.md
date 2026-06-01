# License Audit

# Hokage Vision Agent License Audit

This audit records the current known license boundaries before restructuring the repository. It is not legal advice.

## Initial Findings

- No root `LICENSE`, `COPYING`, or `NOTICE` file was found.
- The repository originally contained a large amount of upstream-like YOLOv5 source code in the root tree, including `detect.py`, `train.py`, `val.py`, `export.py`, `hubconf.py`, `models/`, `utils/`, `classify/`, `segment/`, and `data/`. This legacy tree has been moved under `legacy/old_project/`.
- Local file headers and repository history suggest the imported YOLOv5 code is from a GPL-3.0-era YOLOv5 tree. Current upstream YOLOv5 uses AGPL-3.0, but this repository should not assume AGPL-only without confirming the exact imported upstream version.
- Git history indicates a root GPL-3.0 `LICENSE` existed in the first commit and was later deleted. The legacy `setup.cfg` now lives under `legacy/old_project/`.
- Project-specific legacy files include `base_ui.py`, `main_window.py`, `main_window.ui`, `test_open_image.py`, `datasets/classes.txt`, and readme/demo images under `legacy/old_project/`.
- The legacy tree includes label files under `legacy/old_project/datasets/labels/` and sample images under `legacy/old_project/data/images/`, but no source manifest or redistribution statement.
- No model weight `.pt` files were found in the initial large-file scan, but the GUI hardcodes `runs/train/exp/weights/best.pt`.

## Proposed License Boundaries

- New Hokage Vision Agent source code: Apache-2.0, pending final confirmation that no legacy YOLOv5 source is copied into `src/hokage_vision`.
- Documentation: CC BY 4.0 may be declared separately if desired.
- Legacy YOLOv5 code: governed by upstream YOLOv5 licensing and isolated under `legacy/old_project/`.
- Model weights: separately licensed and distributed through releases or manual download scripts only after license review.
- Dataset images: not redistributed unless rights are verified.
- Dataset annotations: separately licensed only after corresponding image rights are reviewed.

## Risk Items Requiring Human Confirmation

- Exact upstream YOLOv5 commit/version used as the base of this repository.
- Whether any project-specific files include copied YOLOv5 code beyond normal imports.
- Legal status and redistribution permission for any Naruto/Hokage dataset images used to produce `legacy/old_project/datasets/labels/`.
- Legal status of `legacy/old_project/readme_images.png` and `legacy/old_project/readme_images/PixPin_2024-05-30_09-03-06.gif`.
- Whether `legacy/old_project/libEGL.dll` can be redistributed in this repository and under which license.
- Whether old notebooks contain embedded outputs or assets that should be removed or isolated.
- Exact license for the historical YOLOv5 version imported here, including whether GPL-3.0 is the correct governing license for the retained legacy snapshot.

## Required Follow-up

- Keep the Apache-2.0 `LICENSE` scoped to newly written Hokage Vision Agent code until legacy isolation is complete.
- Keep `LICENSES/README.md` updated with source, docs, legacy, data, annotations, model weights, and binary asset boundaries.
- Preserve or reference the applicable upstream YOLOv5 license for legacy code.
- Keep `THIRD_PARTY_NOTICES.md` updated as dependencies are introduced.
