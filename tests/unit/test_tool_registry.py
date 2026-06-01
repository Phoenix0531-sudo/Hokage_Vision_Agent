from hokage_vision.agents.registry import ToolRegistry


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
