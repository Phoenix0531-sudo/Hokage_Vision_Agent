from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class AppConfig(BaseModel):
    name: str = "Hokage Vision Agent"
    language: str = "zh-CN"
    output_dir: Path = Path("runs")
    portfolio_mode: bool = True


class ModelConfig(BaseModel):
    backend: str = "mock"
    path: Path | None = None
    device: str = "auto"
    conf_threshold: float = 0.25
    iou_threshold: float = 0.45
    image_size: int = 640
    classes: list[str] = Field(default_factory=lambda: ["obito", "naruto", "gaara"])

    @field_validator("conf_threshold", "iou_threshold")
    @classmethod
    def validate_threshold(cls, value: float) -> float:
        if not 0 <= value <= 1:
            msg = "threshold values must be between 0 and 1"
            raise ValueError(msg)
        return value


class AgentConfig(BaseModel):
    provider: str = "rule_based"
    enable_llm: bool = False
    allowed_tools: list[str] = Field(default_factory=list)
    max_steps: int = 8
    shell_access: bool = False
    dry_run_by_default: bool = True


class UiConfig(BaseModel):
    language: str = "zh-CN"
    theme: str = "dark"
    allow_theme_switch: bool = True
    allow_language_switch: bool = True
    window_width: int = 1280
    window_height: int = 860


class ApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class TrainingConfig(BaseModel):
    default_epochs: int = 1
    smoke_test_epochs: int = 1
    dry_run_by_default: bool = True


class DataConfig(BaseModel):
    allow_web_download: bool = False
    require_manifest: bool = True
    require_license_review: bool = True
    allow_redistribution_by_default: bool = False


class Settings(BaseModel):
    app: AppConfig = Field(default_factory=AppConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    ui: UiConfig = Field(default_factory=UiConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    data: DataConfig = Field(default_factory=DataConfig)
