from __future__ import annotations

from pathlib import Path


def training_job_path(output_dir: Path) -> Path:
    return Path(output_dir) / "training-job.json"
