from typing import AsyncIterator

from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    model: str
    prompt: str
    system: str | None = None
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)


class GenerationResult(BaseModel):
    text: str
    latency_ms: int = Field(..., ge=0)
    model: str
    provider: str
    error: str | None = None


class GenerationChunk(BaseModel):
    delta: str
    done: bool = False
