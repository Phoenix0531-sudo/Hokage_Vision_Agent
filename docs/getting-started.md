# Getting Started

Docker is the primary development, test, and build path for Hokage Vision Agent.

```bash
docker compose build
docker compose run --rm test
```

The default configuration is stored in `configs/app.default.yaml`. The default backend is `mock`, which keeps tests and demos independent from GPU, private data, and real model weights.

The mock backend returns deterministic detections for `obito`, `naruto`, and `gaara`, so the CLI, API, GUI, and agent layers can be tested before real model weights are available.
