from pathlib import Path

from hokage_vision.agents.registry import ToolRegistry
from hokage_vision.agents.tools import create_default_tool_registry


def test_tool_registry_registers_and_calls_allowed_tool() -> None:
    registry = ToolRegistry(allowed_tools=["echo"])
    registry.register("echo", "Echo arguments.", lambda arguments: {"value": arguments["value"]})

    assert registry.list_tools() == ["echo"]
    assert registry.call("echo", {"value": "ok"}) == {"value": "ok"}


def test_tool_registry_blocks_unallowed_tool() -> None:
    registry = ToolRegistry(allowed_tools=["safe"])
    registry.register("unsafe", "Unsafe.", lambda arguments: arguments)

    try:
        registry.call("unsafe", {})
    except PermissionError as exc:
        assert "not allowed" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected PermissionError")


def test_default_tools_auto_label_and_generate_report(tmp_path: Path) -> None:
    registry = create_default_tool_registry()
    labels = registry.call(
        "auto_label_with_model",
        {"images": "examples/images", "output": str(tmp_path / "labels")},
    )
    report = registry.call("generate_report", {"output": str(tmp_path / "report.md")})

    assert labels["review_required"] is True
    assert labels["model"] == "mock"
    assert report["status"] == "success"
    assert (tmp_path / "report.md").exists()
