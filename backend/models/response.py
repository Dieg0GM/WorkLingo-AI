from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


class TranslationResponse(BaseModel):
    model: str
    provider: str
    translated: str
    latency_ms: int = Field(..., ge=0)
    error: str | None = None


class CompareResult(BaseModel):
    model: str
    provider: str
    translated: str
    latency_ms: int = Field(..., ge=0)
    error: str | None = None


class CompareResponse(BaseModel):
    results: list[CompareResult]


class StreamChunk(BaseModel):
    model: str
    provider: str
    delta: str
    done: bool = False
