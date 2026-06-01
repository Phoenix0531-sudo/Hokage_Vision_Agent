from hokage_vision.agents.providers.rule_based import RuleBasedAgent


def test_rule_based_agent_detects_folder() -> None:
    response = RuleBasedAgent().run("检测 examples/images 里的图片")

    assert response.tool_calls[0].name == "detect_folder"
    assert response.tool_calls[0].status == "success"
    assert response.tool_calls[0].result["count"] >= 1


def test_rule_based_agent_refuses_out_of_scope_task() -> None:
    response = RuleBasedAgent().run("帮我查天气")

    assert response.tool_calls == []
    assert "refused" in response.message
