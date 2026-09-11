"""CPU inference speed benchmark utilities.

``benchmark_fps`` times real or mock model inference over a set of images and
reports latency plus derived frames-per-second figures.
"""

from __future__ import annotations

import time
from collections.abc import Iterable
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any

from hokage_vision.vision.backends.base import VisionBackend


def benchmark_fps(
    backend: VisionBackend,
    image_paths: Iterable[Path],
    *,
    warmup: int = 3,
    repeats: int = 10,
) -> dict[str, Any]:
    """Time ``backend.predict_image`` over ``image_paths``.

    Each image is predicted ``repeats`` times after ``warmup`` untimed warm-up
    calls. Returns latency statistics (ms) and FPS derived from them.
    """
    paths = [Path(p) for p in image_paths]
    if not paths:
        msg = "benchmark_fps requires at least one image."
        raise ValueError(msg)

    backend.load()
    for _ in range(warmup):
        backend.predict_image(paths[0])

    per_image_ms: list[list[float]] = []
    for path in paths:
        timings: list[float] = []
        for _ in range(repeats):
            start = time.perf_counter()
            backend.predict_image(path)
            timings.append((time.perf_counter() - start) * 1000.0)
        per_image_ms.append(timings)

    flat_ms = [ms for timings in per_image_ms for ms in timings]
    latency_ms = mean(flat_ms)
    fps = 1000.0 / latency_ms if latency_ms > 0 else 0.0

    return {
        "backend": type(backend).__name__,
        "images": len(paths),
        "repeats": repeats,
        "warmup": warmup,
        "fps": round(fps, 2),
        "fps_by_image": [
            round(1000.0 / mean(timings), 2) if mean(timings) > 0 else 0.0
            for timings in per_image_ms
        ],
        "latency_ms_mean": round(mean(flat_ms), 3),
        "latency_ms_median": round(median(flat_ms), 3),
        "latency_ms_stdev": round(stdev(flat_ms), 3) if len(flat_ms) > 1 else 0.0,
        "latency_ms_min": round(min(flat_ms), 3),
        "latency_ms_max": round(max(flat_ms), 3),
    }
