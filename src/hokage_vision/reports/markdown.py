from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from hokage_vision import __version__


def generate_markdown_report(
    title: str,
    output: Path,
    *,
    summary: dict[str, Any] | None = None,
    tool_results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary = summary or {}
    tool_results = tool_results or []

    lines = [
        f"# {title}",
        "",
        "- Project: Hokage Vision Agent",
        f"- Version: {__version__}",
        "- Scope: research, portfolio, and local engineering workflow",
        "",
        "## Summary",
        "",
    ]
    if summary:
        for key, value in summary.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No additional summary was provided.")

    if tool_results:
        lines.extend(["", "## Tool Results", ""])
        for index, result in enumerate(tool_results, start=1):
            lines.append(f"### Result {index}")
            lines.append("")
            lines.append("```yaml")
            lines.append(yaml.safe_dump(_jsonable(result), sort_keys=False, allow_unicode=True))
            lines.append("```")

    lines.extend(
        [
            "",
            "## Data And License Notes",
            "",
            "- YOLO/CV models perform visual detection; the Agent only orchestrates project tools.",
            "- Historical Naruto/Hokage data and weights are research-only, non-commercial, "
            "and not redistributed by default.",
            "- Review dataset and model provenance before publishing artifacts.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")
    return {"status": "success", "path": str(output), "summary": summary}


def summarize_detections(results: list[dict[str, Any]]) -> dict[str, Any]:
    labels: Counter[str] = Counter()
    total = 0
    for result in results:
        for detection in result.get("detections", []):
            labels[str(detection.get("label", "unknown"))] += 1
            total += 1
    return {"files": len(results), "detections": total, "classes": dict(sorted(labels.items()))}


def _jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value
