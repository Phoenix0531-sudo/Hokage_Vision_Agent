# Training

Training is safe by default.

```bash
hokage-vision train smoke
hokage-vision train yolo --data configs/dataset.example.yaml --epochs 1 --dry-run
```

`train smoke` runs a lightweight mock workflow and does not produce real weights. `train yolo` defaults to dry-run planning. Real execution requires an explicitly valid dataset and the training extra.

Do not publish trained weights until the training data source, redistribution rights, intended use, metrics, and license are documented. Historical Hokage/Naruto weights are treated as research and portfolio artifacts only and non-commercial.
