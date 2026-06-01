from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from hokage_vision.training.jobs import TrainingJob


def run_smoke_training(
    output_dir: Path = Path("runs/smoke-train"), epochs: int = 1
) -> dict[str, object]:
    job = TrainingJob(
        name="hokage-yolo-smoke",
        status="completed",
        dry_run=False,
        output_dir=output_dir,
        parameters={"epochs": epochs, "backend": "mock", "device": "cpu"},
        metrics={"map50": None, "precision": None, "recall": None},
        message="Smoke training completed with mock workflow; no real model weights were produced.",
    )
    return asdict(job)
