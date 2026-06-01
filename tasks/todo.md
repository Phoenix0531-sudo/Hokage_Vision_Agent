# Hokage Vision Agent Refactor Plan

This checklist tracks the staged migration from the legacy YOLOv5 + PySide6 project to the portfolio-ready Hokage Vision Agent project. Each phase must remain reviewable and end with a focused commit.

- [x] Phase 0: Project audit and license audit
- [x] Phase 1: Docker-first project skeleton
- [ ] Phase 2: Configuration system and core detection types
- [ ] Phase 3: Mock backend, rendering, and inference service
- [ ] Phase 4: CLI
- [ ] Phase 5: Agent tool registry and rule-based provider
- [ ] Phase 6: Dataset manifest, validation, and annotation helpers
- [ ] Phase 7: Training skeleton and smoke training
- [ ] Phase 8: Model registry, evaluation, and comparison
- [ ] Phase 9: Ultralytics and legacy YOLOv5 backends
- [ ] Phase 10: Modern PySide6 desktop interface
- [ ] Phase 11: FastAPI service
- [ ] Phase 12: Python package build workflow
- [ ] Phase 13: Desktop executable build workflow
- [ ] Phase 14: CI, documentation, release, and governance
- [ ] Phase 15: Final portfolio polish

## Working Rules

- Keep commits small and use Conventional Commits.
- Do not commit model weights, private datasets, API keys, or generated training output.
- Keep the legacy YOLOv5 code isolated from the new `src/hokage_vision` package.
- Use mock backends for CI, GUI smoke tests, API smoke tests, and agent tests.
- Default real training to dry-run unless the user explicitly asks for execution.
- Do not add web scraping or redistribution of copyrighted Naruto/Hokage imagery.

## Review

### Phase 0

- Added migration, license audit, legacy, and third-party notice documents.
- Confirmed the repository currently has upstream-like YOLOv5 code mixed with project-specific PySide6 GUI files.
- Confirmed there is no root `LICENSE` file in the current repository.
- Confirmed hardcoded local Qt plugin and `runs/train/exp/weights/best.pt` paths in the legacy GUI.
- No old code was moved or deleted in this phase.

### Phase 1

- Added `pyproject.toml`, the initial `src/hokage_vision` package, app entrypoint placeholders, tests, Dockerfile, Docker Compose services, Dev Container config, Makefile, `.env.example`, `.editorconfig`, bilingual README placeholders, and MkDocs skeleton.
- Kept legacy YOLOv5 files in place; no old code was moved or deleted.
- Docker build initially exposed local daemon/network instability and heavy dependency cost; the final base image installs Python dev dependencies but avoids apt system packages in the core test image.
- `test` service disables pytest plugin autoload so non-GUI tests do not require Qt bindings. GUI tests will use the separate `gui-test` service.
- Verified `docker compose build` and Docker package import.
