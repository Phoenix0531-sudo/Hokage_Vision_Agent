from __future__ import annotations

from typing import Any

from hokage_vision.agents.providers.langgraph_provider import LangGraphProvider
from hokage_vision.agents.providers.openai_provider import OpenAIProvider
from hokage_vision.agents.providers.rule_based import RuleBasedAgent
from hokage_vision.agents.registry import ToolRegistry

SUPPORTED_AGENT_PROVIDERS = ("rule_based", "openai", "langgraph")


def create_agent(
    provider: str = "rule_based",
    registry: ToolRegistry | None = None,
    **kwargs: Any,
) -> RuleBasedAgent | OpenAIProvider | LangGraphProvider:
    """Build an agent by provider name; extra kwargs go to the provider ctor."""
    name = provider.strip().lower()
    if name == "rule_based":
        return RuleBasedAgent(registry)
    if name == "openai":
        return OpenAIProvider(registry, **kwargs)
    if name == "langgraph":
        return LangGraphProvider(registry, **kwargs)
    msg = f"Unknown agent provider: {provider}. Supported providers: {', '.join(SUPPORTED_AGENT_PROVIDERS)}."
    raise ValueError(msg)


__all__ = ["SUPPORTED_AGENT_PROVIDERS", "create_agent"]
