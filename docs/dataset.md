# Dataset Format

Datasets use YOLO label format with a manifest that records source and license information.

Example manifest:

```yaml
dataset:
  name: hokage-vision-sample
  version: 0.1.0
  description: Sample dataset manifest for local training.
  redistribution_allowed: false

sources:
  - id: sample-local-001
    type: user_provided
    path: data/raw/user_images
    license: unknown
    redistribution_allowed: false
    notes: User-provided local images. Do not commit raw images.

classes:
  - obito
  - naruto
  - gaara

annotations:
  format: yolo
  reviewed: false
  reviewer: null
```

## Validation Checks

The dataset validator checks split paths, images, labels, YOLO label line format, class bounds, normalized bounding boxes, empty labels, class distribution, missing labels, manifest presence, source records, and redistribution fields.

```bash
hokage-vision dataset validate configs/dataset.example.yaml
```

## Adding Classes

Adding a new character requires new data, verified rights, bounding-box annotations, class name updates, dataset YAML updates, retraining or fine-tuning, evaluation, model registry updates, and documentation updates. The Agent can help orchestrate these steps, but it cannot create legal data or reliable new classes from nothing.
