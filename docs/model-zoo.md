# Model Zoo

Model weights are external artifacts. They are not committed to this repository.

Use the registry to track local or release-provided model metadata:

```bash
hokage-vision model list
hokage-vision model compare --models models/a.pt models/b.pt --mock
```

Before publishing weights, confirm training data rights, model license, class list, metrics, and release notes. Historical Hokage/Naruto weights are research and portfolio artifacts only, non-commercial, and not redistributed by default because their training data provenance is not fully documented.

Real backends:

- `mock`: default for tests and demos.
- `ultralytics`: modern Ultralytics YOLO weights, requires `pip install -e ".[train]"`.
- `yolov5_legacy`: compatibility boundary for old YOLOv5 weights after legacy source isolation.

No backend hardcodes `runs/train/exp/weights/best.pt`.
