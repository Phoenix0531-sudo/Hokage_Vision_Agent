# Roadmap

## Near Term

- Keep mock-backed CLI, GUI, API, Agent, and tests green.
- Add a Docker `train` profile so real training dependencies stay separate from the default CI/test image.
- Capture final GUI screenshots and CLI demo images from the themed desktop app.
- Keep MkDocs, CI, Docker, package, and desktop build workflows green.

## Model and Data

- Publish only reviewed model metadata and weights with clear licenses and model cards.
- Add richer dataset statistics and review workflows.
- Expand evaluation and model comparison reports after real data is approved.
- Add a documented path for users to import local, non-redistributed screenshots into `data/raw`.

## Desktop and API

- Improve desktop packaging across Linux, Windows, and macOS.
- Keep API lightweight and local-first.
- Avoid online inference demos through GitHub Pages.

## Agent

- Keep the default provider rule-based and API-key-free.
- Add optional LLM providers only behind allowlisted tools and explicit user confirmation for expensive operations.
- Add richer natural-language parsing for dataset paths, training configs, and model registry operations without granting shell access.
