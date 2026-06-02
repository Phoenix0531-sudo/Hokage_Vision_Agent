# Model Card: `<model-name>`

## Release Status

- Status: `draft | reviewed-external | released`
- Version: `TBD`
- Registry entry: `models/registry.json`
- Weight path or release URL: `TBD`
- SHA256: `TBD`

## Intended Use

This model is intended for local research, portfolio demonstration, and controlled anime character detection experiments. It is not a public dataset redistribution mechanism and is not cleared for commercial use unless the training data and weight license explicitly allow it.

## Classes

- `obito`
- `naruto`
- `gaara`

## Data Provenance

- Dataset manifest: `TBD`
- Image sources: `TBD`
- Redistribution allowed: `TBD`
- Annotation review status: `TBD`
- Known excluded data: copyrighted screenshots or private captures without documented rights.

## Training Configuration

- Backend: `ultralytics | yolov5_legacy`
- Base model: `TBD`
- Epochs: `TBD`
- Batch size: `TBD`
- Image size: `TBD`
- Device: `TBD`
- Output directory: `TBD`

## Evaluation

- Evaluation dataset: `TBD`
- mAP50: `TBD`
- mAP50-95: `TBD`
- Precision: `TBD`
- Recall: `TBD`
- Latency: `TBD`
- Model size: `TBD`

## Limitations

- Performance depends on reviewed, representative training images and bounding-box annotations.
- Adding a new character requires new data, new labels, updated class names, retraining, evaluation, and registry updates.
- The Agent can orchestrate training and evaluation, but it cannot create legal data or reliable new classes from nothing.

## License Notes

- Model weight license: `TBD`
- Training data license: `TBD`
- Annotation license: `TBD`
- Redistribution notes: `TBD`
