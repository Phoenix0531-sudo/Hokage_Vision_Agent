from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from hokage_vision.agents.registry import ToolRegistry
from hokage_vision.core.types import ModelInfo
from hokage_vision.data.annotation import assist_annotation
from hokage_vision.data.manifest import create_dataset_manifest
from hokage_vision.data.validation import validate_yolo_dataset
from hokage_vision.training.registry import ModelRegistry
from hokage_vision.training.smoke import run_smoke_training
from hokage_vision.training.trainer import run_yolo_training
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.evaluation import evaluate_model
from hokage_vision.vision.inference import InferenceService
from hokage_vision.vision.model_compare import compare_model_paths

DEFAULT_ALLOWED_TOOLS = [
    "detect_image",
    "detect_video",
    "detect_folder",
    "validate_dataset",
    "create_dataset_manifest",
    "assist_annotation",
    "auto_label_with_model",
    "train_model",
    "smoke_train",
    "evaluate_model",
    "compare_models",
    "list_models",
    "register_model",
    "generate_report",
    "project_health_check",
]


def create_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry(allowed_tools=DEFAULT_ALLOWED_TOOLS)
    registry.register("detect_image", "Detect objects in one image.", _detect_image)
    registry.register("detect_folder", "Detect objects in a local folder.", _detect_folder)
    registry.register("detect_video", "Detect objects in a local video.", _detect_video)
    registry.register("validate_dataset", "Validate a YOLO dataset.", _validate_dataset)
    registry.register(
        "create_dataset_manifest",
        "Create a dataset manifest.",
        _create_dataset_manifest,
    )
    registry.register("assist_annotation", "Prepare annotation assistance.", _assist_annotation)
    registry.register(
        "auto_label_with_model",
        "Generate model-assisted candidate labels.",
        _placeholder("auto_label_with_model"),
    )
    registry.register("train_model", "Plan or run model training.", _train_model)
    registry.register("smoke_train", "Run smoke training.", _smoke_train)
    registry.register("evaluate_model", "Evaluate a model.", _evaluate_model)
    registry.register("compare_models", "Compare model weights.", _compare_models)
    registry.register("list_models", "List registered models.", _list_models)
    registry.register("register_model", "Register a model.", _register_model)
    registry.register(
        "generate_report", "Generate a report on explicit request.", _placeholder("generate_report")
    )
    registry.register("project_health_check", "Check project health.", _project_health_check)
    return registry


def _service() -> InferenceService:
    return InferenceService(MockBackend())


def _detect_image(arguments: dict[str, Any]) -> dict[str, Any]:
    path = Path(arguments["path"])
    return asdict(_service().detect_image(path))


def _detect_folder(arguments: dict[str, Any]) -> dict[str, Any]:
    path = Path(arguments["path"])
    results = _service().detect_folder(path)
    return {"count": len(results), "results": [asdict(result) for result in results]}


def _detect_video(arguments: dict[str, Any]) -> dict[str, Any]:
    path = Path(arguments["path"])
    return asdict(_service().detect_video(path))


def _project_health_check(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "ok",
        "scope": "project",
        "checks": ["config", "mock_backend", "cli"],
        "dry_run": True,
    }


def _validate_dataset(arguments: dict[str, Any]) -> dict[str, Any]:
    path = Path(arguments.get("path") or arguments.get("task", "configs/dataset.example.yaml"))
    if not path.exists():
        path = Path("configs/dataset.example.yaml")
    return validate_yolo_dataset(path).__dict__


def _create_dataset_manifest(arguments: dict[str, Any]) -> dict[str, Any]:
    images = Path(arguments.get("images", "data/raw"))
    output = Path(arguments.get("output", "data/manifests/local.yaml"))
    return create_dataset_manifest(images, output).model_dump(mode="json")


def _assist_annotation(arguments: dict[str, Any]) -> dict[str, Any]:
    images = Path(arguments.get("images", "examples/images"))
    output = Path(arguments.get("output", "data/interim/labels"))
    return assist_annotation(images, output)


def _smoke_train(arguments: dict[str, Any]) -> dict[str, Any]:
    return run_smoke_training(epochs=int(arguments.get("epochs", 1)))


def _train_model(arguments: dict[str, Any]) -> dict[str, Any]:
    data = Path(arguments.get("data", "configs/dataset.example.yaml"))
    return run_yolo_training(data, dry_run=True)


def _list_models(arguments: dict[str, Any]) -> dict[str, Any]:
    return {"models": ModelRegistry().list_models()}


def _register_model(arguments: dict[str, Any]) -> dict[str, Any]:
    model = ModelInfo(
        name=str(arguments.get("name", "hokage-yolo-local")),
        version=str(arguments.get("version", "0.1.0")),
        path=Path(arguments["path"]) if arguments.get("path") else None,
        backend=str(arguments.get("backend", "ultralytics")),
        classes=["obito", "naruto", "gaara"],
    )
    return ModelRegistry().register(model)


def _evaluate_model(arguments: dict[str, Any]) -> dict[str, Any]:
    return evaluate_model(Path(arguments.get("model", "models/sample.pt")), mock=True)


def _compare_models(arguments: dict[str, Any]) -> dict[str, Any]:
    models = [Path(item) for item in arguments.get("models", ["models/a.pt", "models/b.pt"])]
    return {"models": compare_model_paths(models, mock=True)}


def _placeholder(name: str):
    def handler(arguments: dict[str, Any]) -> dict[str, Any]:
        return {"status": "placeholder", "tool": name, "arguments": arguments, "dry_run": True}

    return handler
