from typing import Literal

from pydantic import BaseModel, Field


Channel = Literal["email", "slack", "chat"]
Tone = Literal["professional", "friendly", "formal"]
Mode = Literal["translate", "compose"]


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    source_language: str = Field(..., min_length=2, max_length=10)
    target_language: str = Field(..., min_length=2, max_length=10)
    channel: Channel = "email"
    tone: Tone = "professional"
    mode: Mode = "translate"
    model: str = Field(..., min_length=1, max_length=100)
    temperature: float | None = Field(None, ge=0.0, le=2.0)


class CompareRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    source_language: str = Field(..., min_length=2, max_length=10)
    target_language: str = Field(..., min_length=2, max_length=10)
    channel: Channel = "email"
    tone: Tone = "professional"
    mode: Mode = "translate"
    models: list[str] = Field(..., min_length=1, max_length=6)
