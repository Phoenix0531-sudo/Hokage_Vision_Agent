from pathlib import Path

from hokage_vision.core.types import ModelInfo
from hokage_vision.training.registry import ModelRegistry


def test_model_registry_registers_model(tmp_path: Path) -> None:
    registry = ModelRegistry(tmp_path / "registry.json")
    record = registry.register(
        ModelInfo("mock-model", "0.1.0", Path("models/mock.pt"), "mock", ["obito"])
    )

    assert record["name"] == "mock-model"
    assert registry.list_models()[0]["backend"] == "mock"
