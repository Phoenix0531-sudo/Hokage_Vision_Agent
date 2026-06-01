from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TrainingJob:
    name: str
    status: str
    dry_run: bool
    output_dir: Path
    parameters: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, float | None] = field(default_factory=dict)
    message: str | None = None
