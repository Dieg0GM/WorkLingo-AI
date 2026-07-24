from typing import Literal

from pydantic import BaseModel, Field


Capability = Literal["chat", "translate", "code", "vision", "tools"]
Speed = Literal["slow", "medium", "fast", "very_fast"]
Quality = Literal["basic", "good", "great", "excellent"]
ProviderStatus = Literal["ok", "down", "missing_key", "invalid_key"]
HealthState = Literal["ok", "degraded", "down"]


class ModelInfo(BaseModel):
    id: str = Field(..., description="Format: provider:model_id")
    provider: str
    display_name: str
    is_free: bool
    context_window: int = Field(..., gt=0)
    capabilities: list[Capability]
    languages: list[str] = Field(default_factory=list)
    speed: Speed
    quality: Quality
    notes: str | None = None


class ProviderInfo(BaseModel):
    name: str
    display_name: str
    configured: bool
    requires_key: bool
    is_free: bool
    base_url: str | None = None
    models: list[ModelInfo] = Field(default_factory=list)


class HealthCheck(BaseModel):
    name: str
    status: ProviderStatus
    latency_ms: int | None = None
    error: str | None = None


class HealthReport(BaseModel):
    status: HealthState
    providers: list[HealthCheck] = Field(default_factory=list)
