"""Import-surface tests for vision re-export stubs."""

from __future__ import annotations


def test_batch_reexports_inference_service() -> None:
    from hokage_vision.vision import batch
    from hokage_vision.vision.inference import InferenceService

    assert batch.InferenceService is InferenceService
    assert batch.__all__ == ["InferenceService"]


def test_video_reexports_video_detection_summary() -> None:
    from hokage_vision.core.types import VideoDetectionSummary
    from hokage_vision.vision import video

    assert video.VideoDetectionSummary is VideoDetectionSummary
    assert video.__all__ == ["VideoDetectionSummary"]
