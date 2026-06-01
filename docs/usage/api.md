# API Usage

The FastAPI service is local-first and uses the mock backend by default. It does not expose real training by default and it does not require an LLM API key.

```bash
docker compose up api
```

OpenAPI docs are available at:

```text
http://localhost:8000/docs
```

Core endpoints:

- `GET /health`
- `GET /models`
- `POST /detect/image`
- `POST /detect/folder`
- `POST /agent/run`
- `POST /dataset/validate`
- `POST /train/smoke`
- `POST /models/compare`

Example local path request:

```bash
curl -X POST http://localhost:8000/detect/image \
  -H "Content-Type: application/json" \
  -d '{"image_path":"examples/images/sample.jpg","backend":"mock"}'
```
