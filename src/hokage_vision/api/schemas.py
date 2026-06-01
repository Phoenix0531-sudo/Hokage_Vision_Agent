from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ImageDetectRequest(BaseModel):
    image_path: Path
    backend: str = "mock"
    save_rendered: bool = False
    save_json: bool = False


class FolderDetectRequest(BaseModel):
    folder: Path
    backend: str = "mock"
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
