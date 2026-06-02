from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ImageDetectRequest(BaseModel):
    image_path: Path
    backend: str = "mock"
    model_path: Path | None = None
    conf_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    iou_threshold: float = Field(default=0.45, ge=0.0, le=1.0)
    image_size: int = Field(default=640, ge=1)
    device: str = "auto"
    save_rendered: bool = False
    save_json: bool = False


class FolderDetectRequest(BaseModel):
    folder: Path
    backend: str = "mock"
    model_path: Path | None = None
    conf_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    iou_threshold: float = Field(default=0.45, ge=0.0, le=1.0)
    image_size: int = Field(default=640, ge=1)
    device: str = "auto"
    recursive: bool = False


class AgentRunRequest(BaseModel):
    task: str = Field(min_length=1)


class DatasetValidateRequest(BaseModel):
    dataset_yaml: Path


class TrainSmokeRequest(BaseModel):
    output_dir: Path = Path("runs/smoke-train")
    epochs: int = Field(default=1, ge=1)


class ModelCompareRequest(BaseModel):
    models: list[Path] = Field(min_length=1)
    mock: bool = True
