from dataclasses import asdict
from pathlib import Path

from hokage_vision.core.types import (
    BoundingBox,
    Detection,
    DetectionResult,
    ModelInfo,
    VideoDetectionSummary,
)


def test_detection_result_dataclass_shape() -> None:
    detection = Detection("naruto", 0.91, BoundingBox(1, 2, 30, 40))
    result = DetectionResult(
        source="sample.jpg",
        detections=[detection],
        width=100,
        height=80,
        rendered_image_path=Path("runs/sample.jpg"),
    )

    assert result.detections[0].label == "naruto"
    assert result.detections[0].box.x2 == 30
    assert asdict(result)["width"] == 100


def test_video_summary_and_model_info_defaults() -> None:
    summary = VideoDetectionSummary("demo.mp4", frame_count=10, processed_frames=2, detections_by_frame=[])
    model = ModelInfo("mock", "0.1.0", None, "mock", ["obito", "naruto", "gaara"])

    assert summary.fps is None
    assert summary.metadata == {}
    assert model.metrics == {}
    assert model.notes is None
