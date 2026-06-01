# Architecture

Hokage Vision Agent separates UI, orchestration, and computer vision execution.

```mermaid
flowchart TD
    CLI["CLI"]
    GUI["PySide6 GUI"]
    API["FastAPI"]
    Agent["RuleBasedAgent"]
    Inference["InferenceService"]
    Tools["ToolRegistry"]
    Backend["VisionBackend"]
    Data["Dataset / Training / Model Registry"]

    CLI --> Inference
    GUI --> Inference
    API --> Inference
    Agent --> Tools
    Tools --> Inference
    Tools --> Data
    Inference --> Backend
    Backend --> Mock["MockBackend"]
    Backend --> Ultra["UltralyticsBackend"]
    Backend --> Legacy["YOLOv5LegacyBackend"]
```

The model backend performs detection. The Agent does not replace YOLO or decide visual labels; it only selects safe project tools such as detection, dataset validation, smoke training, evaluation, comparison, and model registry updates.

## Boundaries

- GUI, CLI, API, and Agent share core dataclasses and services.
- The default mock backend keeps CI independent from GPU and private weights.
- Real training and destructive operations default to dry-run.
- Legacy YOLOv5 compatibility remains behind `YOLOv5LegacyBackend` and must not be copied into the new package.
