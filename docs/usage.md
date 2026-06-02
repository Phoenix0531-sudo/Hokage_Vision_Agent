# Usage

## CLI

```bash
hokage-vision --help
hokage-vision detect image examples/images/sample.jpg --backend mock
hokage-vision detect folder examples/images --backend mock
hokage-vision dataset validate configs/dataset.example.yaml
hokage-vision train yolo --data configs/dataset.example.yaml --epochs 1 --dry-run
hokage-vision agent run "检测 examples/images 里的图片"
```

Real model weights stay external. After placing a reviewed weight file under `models/`,
run it explicitly:

```bash
hokage-vision detect image examples/images/sample.jpg --backend ultralytics --model-path models/your-model.pt --device cpu
```

## GUI

The PySide6 desktop app includes Overview, Image Detection, Video Detection, Batch Detection, Agent Assistant, Settings, and About pages. GUI smoke tests use the mock backend and run headlessly.

```bash
hokage-vision gui
```

## API

The FastAPI service is local-first, mock-backed by default, and does not expose real training by default.

```bash
docker compose up api
```

OpenAPI docs are available at `http://localhost:8000/docs`.

Core endpoints:

- `GET /health`
- `GET /models`
- `POST /detect/image`
- `POST /detect/folder`
- `POST /agent/run`
- `POST /dataset/validate`
- `POST /train/smoke`
- `POST /models/compare`

## Agent

The default Agent is rule-based, runs without API keys, and can only call allowlisted project tools. It refuses unrelated writing, weather lookup, arbitrary shell execution, API key disclosure, and copyrighted image scraping.

`generate_report` is only selected when the user explicitly asks for a report.

Training orchestration is safe by default:

```bash
hokage-vision agent run "训练模型"
```

This calls the allowlisted `train_model` tool and returns a dry-run training plan. It does not start a long-running real training job without explicit execution.

## Training

Training is safe by default.

```bash
hokage-vision train smoke
hokage-vision train yolo --data configs/dataset.example.yaml --epochs 1 --dry-run
```

Real training requires a valid YOLO dataset, reviewed data rights, and the training extra. Historical Hokage/Naruto weights are research and portfolio artifacts only, non-commercial, and not redistributed by default.

## Interview Walkthrough

Use this sequence to demonstrate the project as an engineering system:

1. Validate the synthetic dataset and manifest.
2. Run mock image detection through the shared inference service.
3. Ask the Agent to plan training.
4. Show GUI smoke tests running headlessly.
5. Start the API and open `/docs`.
