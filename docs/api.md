# API Reference

The FastAPI service (`hokage-vision api` / `docker compose up api`) is local-first,
mock-backed by default, and does not expose real training. Interactive OpenAPI docs
are served at `http://localhost:8000/docs`.

All request and response bodies are JSON. Hokage vision errors map to
`400` with a human-readable `detail`; invalid payloads map to `422`.

## Endpoints

### `GET /health`

Liveness probe. Returns service status metadata (version, uptime fields).

```bash
curl http://localhost:8000/health
```

### `GET /models`

Lists models registered in the local registry (`models/registry.json`).

```json
{ "models": [ { "name": "...", "version": "...", "path": "...", "backend": "..." } ] }
```

### `POST /detect/image`

Detect objects in one image.

Request body:

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `image_path` | path | required | Image file to run |
| `backend` | str | `mock` | `mock`, `ultralytics`, `yolov5_legacy`, ... |
| `model_path` | path | `null` | Required for real backends |
| `conf_threshold` | float | `0.25` | 0.0–1.0 |
| `iou_threshold` | float | `0.45` | 0.0–1.0 |
| `image_size` | int | `640` | Must match ONNX export size for `.onnx` models |
| `device` | str | `auto` | `cpu`, `cuda:0`, ... |
| `save_rendered` | bool | `false` | Write rendered image next to the input |
| `save_json` | bool | `false` | Write detections JSON next to the input |

Response: a `DetectionResult` object — `image_path`, `width`, `height`,
`detections` (`label`, `confidence`, `bbox`), and `metadata`
(backend, model path, timings).

```bash
curl -X POST http://localhost:8000/detect/image \
  -H "Content-Type: application/json" \
  -d '{"image_path": "examples/images/sample.jpg", "backend": "mock"}'
```

Unsupported backend names and missing model files return `400`.

### `POST /detect/folder`

Detect objects over a folder of images.

Same fields as `/detect/image` plus `recursive` (default `false`).
Response: `{"results": [DetectionResult, ...]}`. A missing folder returns `400`.

### `POST /agent/run`

Run one agent task.

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `task` | str | required | Natural-language task (min length 1) |
| `provider` | str | `rule_based` | `rule_based`, `openai`, `langgraph` |

The rule-based provider runs offline and refuses out-of-scope tasks
(writing, weather, shell, credentials) with an explanatory message and
no tool calls. `openai` requires `OPENAI_API_KEY`; `langgraph` requires
the `llm` extra (`pip install -e ".[llm]"`). Missing keys or extras map
to `400` with an install/config hint.

Response: an `AgentResponse` — `message`, `tool_calls`, `artifacts`,
`suggestions`, `errors`.

### `POST /dataset/validate`

Validate a YOLO dataset yaml (paths exist, labels parse, manifest present).
Returns a `DatasetValidationReport` with `valid`, `issues`,
`invalid_labels`, and `missing_labels`. Note: an unparseable or missing
yaml still returns HTTP `200` with `valid: false` and issue strings.

### `POST /train/smoke`

Run the built-in smoke training job (mock model, tiny synthetic data — no real
weights are produced).

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `output_dir` | path | `runs/smoke-train` | Output location recorded in the job payload |
| `epochs` | int | `1` | >= 1 |

Real YOLO training is intentionally not exposed over HTTP; use the CLI
(`hokage-vision train yolo ...`) locally after data review.

### `POST /models/compare`

Compare model files by size and recorded metadata.

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `models` | list[path] | required | At least one path |
| `mock` | bool | `true` | Mock mode never touches real weights |

Missing files are reported with `size_bytes: null` instead of failing.
