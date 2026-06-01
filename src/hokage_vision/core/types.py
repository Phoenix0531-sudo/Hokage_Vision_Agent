from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    box: BoundingBox


@dataclass
class DetectionResult:
    source: str
    detections: list[Detection]
    width: int | None = None
    height: int | None = None
    rendered_image_path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VideoDetectionSummary:
    source: str
    frame_count: int
    processed_frames: int
    detections_by_frame: list[DetectionResult]
    fps: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelInfo:
    name: str
    version: str
    path: Path | None
    backend: str
    classes: list[str]
    metrics: dict[str, float | None] = field(default_factory=dict)
    notes: str | None = None
