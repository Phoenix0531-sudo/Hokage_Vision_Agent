from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from hokage_vision.core.types import ModelInfo


def training_job_path(output_dir: Path) -> Path:
    return Path(output_dir) / "training-job.json"


class ModelRegistry:
    def __init__(self, path: Path = Path("models/registry.json")) -> None:
        self.path = Path(path)

    def list_models(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return list(data.get("models", []))

    def register(self, model: ModelInfo, *, license_name: str = "TBD") -> dict[str, object]:
        records = self.list_models()
        record = asdict(model)
        record["path"] = str(model.path) if model.path else None
        record["created_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        record["license"] = license_name
        records = [
            item
            for item in records
            if not (item.get("name") == model.name and item.get("version") == model.version)
        ]
        records.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"models": records}, indent=2), encoding="utf-8")
        return record
