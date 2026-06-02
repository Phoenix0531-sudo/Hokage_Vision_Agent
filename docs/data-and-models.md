# Data And Models

Hokage Vision Agent does not download, scrape, or redistribute copyrighted anime images by default.

## Dataset Governance

Dataset work must start from a manifest that records local source paths, license status, redistribution permission, classes, and annotation review state. Unknown licenses are treated as not redistributable.

Legacy Naruto/Hokage screenshots, local captures, labels, and historical weights are local research material only. Do not publish them as a reusable public dataset, do not use them commercially, and do not upload them to releases until rights and redistribution terms are documented.

## Dataset Format

Datasets use YOLO label format plus a manifest:

```yaml
dataset:
  name: hokage-vision-sample
  version: 0.1.0
  redistribution_allowed: false

sources:
  - id: sample-local-001
    type: user_provided
    path: data/raw/user_images
    license: unknown
    redistribution_allowed: false

classes:
  - obito
  - naruto
  - gaara

annotations:
  format: yolo
  reviewed: false
```

Validate a dataset:

```bash
hokage-vision dataset validate configs/dataset.example.yaml
```

## Annotation Assistance

Annotation assistance generates candidate YOLO labels and always marks them as requiring human review.

```bash
hokage-vision annotation assist --images examples/images --output data/interim/labels --review-required
```

## Model Registry

Model weights are external artifacts and are not committed to git.

```bash
hokage-vision model list
hokage-vision model compare --models models/a.pt models/b.pt --mock
```

Before publishing weights, confirm training data rights, model license, class list, metrics, and release notes.

## Adding Classes

Adding a new character requires new images, verified rights, bounding-box annotations, class name updates, dataset YAML updates, retraining or fine-tuning, evaluation, model registry updates, and documentation updates. The Agent can help orchestrate these steps, but it cannot create legal data or reliable new classes from nothing.
