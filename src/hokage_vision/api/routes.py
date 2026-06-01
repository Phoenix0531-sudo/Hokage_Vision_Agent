from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from hokage_vision import __version__
from hokage_vision.agents.providers.rule_based import RuleBasedAgent
from hokage_vision.api.schemas import (
    AgentRunRequest,
    DatasetValidateRequest,
    FolderDetectRequest,
    ImageDetectRequest,
    ModelCompareRequest,
    TrainSmokeRequest,
)
from hokage_vision.core.errors import HokageVisionError
from hokage_vision.data.validation import validate_yolo_dataset
from hokage_vision.training.registry import ModelRegistry
from hokage_vision.training.smoke import run_smoke_training
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.inference import InferenceService
from hokage_vision.vision.model_compare import compare_model_paths

router = APIRouter()


def _service_for_backend(backend: str) -> InferenceService:
    if backend != "mock":
        raise HTTPException(status_code=400, detail="API currently supports the mock backend by default.")
    return InferenceService(MockBackend())


def _encode(value: object) -> object:
    return jsonable_encoder(value)


@router.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "app": "Hokage Vision Agent",
        "version": __version__,
        "backend": "mock",
    }


@router.get("/models")
def models() -> dict[str, object]:
    return {"models": ModelRegistry().list_models()}


@router.post("/detect/image")
def detect_image(request: ImageDetectRequest) -> object:
    try:
        result = _service_for_backend(request.backend).detect_image(
            request.image_path,
            save_rendered=request.save_rendered,
            save_json=request.save_json,
        )
    except HokageVisionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _encode(asdict(result))


@router.post("/detect/folder")
def detect_folder(request: FolderDetectRequest) -> object:
    try:
        results = _service_for_backend(request.backend).detect_folder(
            request.folder,
            recursive=request.recursive,
        )
    except HokageVisionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _encode({"results": [asdict(result) for result in results]})


@router.post("/agent/run")
def agent_run(request: AgentRunRequest) -> object:
    return _encode(asdict(RuleBasedAgent().run(request.task)))


@router.post("/dataset/validate")
def dataset_validate(request: DatasetValidateRequest) -> object:
    return _encode(asdict(validate_yolo_dataset(request.dataset_yaml)))


@router.post("/train/smoke")
def train_smoke(request: TrainSmokeRequest) -> object:
    return _encode(run_smoke_training(output_dir=request.output_dir, epochs=request.epochs))


@router.post("/models/compare")
def model_compare(request: ModelCompareRequest) -> object:
    return _encode({"models": compare_model_paths(request.models, mock=request.mock)})
