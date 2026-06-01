from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class DatasetInfo(BaseModel):
    name: str
    version: str = "0.1.0"
    description: str = ""
    redistribution_allowed: bool = False


class DatasetSource(BaseModel):
    id: str
    type: str = "user_provided"
    path: Path
    license: str = "unknown"
    redistribution_allowed: bool = False
    notes: str = ""


class AnnotationInfo(BaseModel):
    format: str = "yolo"
    reviewed: bool = False
    reviewer: str | None = None


class DatasetManifest(BaseModel):
    dataset: DatasetInfo
    sources: list[DatasetSource] = Field(default_factory=list)
    classes: list[str] = Field(default_factory=list)
    annotations: AnnotationInfo = Field(default_factory=AnnotationInfo)
