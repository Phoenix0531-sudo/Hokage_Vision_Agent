from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import DetectionResult, VideoDetectionSummary
from hokage_vision.vision.backends.base import VisionBackend
from hokage_vision.vision.rendering import render_detections

ProgressCallback = Callable[[int, int], None]


class InferenceService:
    def __init__(
        self,
        backend: VisionBackend,
        image_extensions: set[str] | None = None,
    ) -> None:
        self.backend = backend
        self.image_extensions = image_extensions or {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    def detect_image(
        self,
        image_path: Path,
        *,
        save_rendered: bool = False,
        save_json: bool = False,
        output_dir: Path | None = None,
    ) -> DetectionResult:
        result = self.backend.predict_image(Path(image_path))
        output_dir = output_dir or Path("runs") / "detect"
        if save_rendered:
            output_dir.mkdir(parents=True, exist_ok=True)
            rendered_path = output_dir / f"{Path(image_path).stem}_mock.jpg"
            render_detections(Path(image_path), result, rendered_path)
            result.rendered_image_path = rendered_path
        if save_json:
            output_dir.mkdir(parents=True, exist_ok=True)
            json_path = output_dir / f"{Path(image_path).stem}.json"
            json_path.write_text(
                json.dumps(asdict(result), default=str, indent=2), encoding="utf-8"
            )
            result.metadata["json_path"] = str(json_path)
        return result

    def detect_folder(
        self,
        folder: Path,
        *,
        recursive: bool = False,
        progress_callback: ProgressCallback | None = None,
    ) -> list[DetectionResult]:
        folder = Path(folder)
        if not folder.exists() or not folder.is_dir():
            msg = f"Image folder does not exist: {folder}"
            raise VisionBackendError(msg)
        pattern = "**/*" if recursive else "*"
        paths = sorted(
            path
            for path in folder.glob(pattern)
            if path.is_file() and path.suffix.lower() in self.image_extensions
        )
        results: list[DetectionResult] = []
        total = len(paths)
        for index, path in enumerate(paths, start=1):
            try:
                results.append(self.detect_image(path))
            except Exception as exc:  # pragma: no cover - kept for folder-level error collection
                results.append(
                    DetectionResult(
                        source=str(path),
                        detections=[],
                        metadata={"error": str(exc)},
                    )
                )
            if progress_callback:
                progress_callback(index, total)
        return results

    def detect_video(
        self,
        video_path: Path,
        *,
        frame_stride: int = 30,
        progress_callback: ProgressCallback | None = None,
    ) -> VideoDetectionSummary:
        try:
            import cv2  # type: ignore[import-not-found]
        except ImportError as exc:
            msg = "Video detection requires opencv-python. Install the vision/video extra when available."
            raise VisionBackendError(msg) from exc

        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            msg = f"Video could not be opened: {video_path}"
            raise VisionBackendError(msg)

        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0) or None
        detections: list[DetectionResult] = []
        frame_index = 0
        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                if frame_index % frame_stride == 0:
                    detections.append(self.backend.predict_frame(frame))
                    if progress_callback:
                        progress_callback(frame_index + 1, frame_count)
                frame_index += 1
        finally:
            capture.release()

        return VideoDetectionSummary(
            source=str(video_path),
            frame_count=frame_count,
            processed_frames=len(detections),
            detections_by_frame=detections,
            fps=fps,
            metadata={"frame_stride": frame_stride},
        )
