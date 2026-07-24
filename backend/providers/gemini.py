import asyncio
import time
from typing import AsyncIterator, ClassVar

from google import genai
from google.genai import types

from backend.models.generation import GenerationChunk, GenerationRequest, GenerationResult
from backend.models.provider import HealthCheck, ModelInfo
from backend.providers.base import BaseProvider


_LANGUAGES = [
    "es", "en", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru",
    "ar", "hi", "nl", "sv", "pl", "tr", "vi", "th", "id", "uk",
]


class GeminiProvider(BaseProvider):
    name: ClassVar[str] = "gemini"
    display_name: ClassVar[str] = "Google Gemini"
    requires_key: ClassVar[bool] = True
    is_free: ClassVar[bool] = True

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._client: genai.Client | None = None

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def list_models(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                id="gemini:gemini-3.6-flash",
                provider="gemini",
                display_name="Gemini 3.6 Flash",
                is_free=True,
                context_window=1_048_576,
                capabilities=["chat", "translate", "code", "vision", "tools"],
                languages=_LANGUAGES,
                speed="very_fast",
                quality="excellent",
                notes="Latest, recommended default",
            ),
            ModelInfo(
                id="gemini:gemini-3.5-flash",
                provider="gemini",
                display_name="Gemini 3.5 Flash",
                is_free=True,
                context_window=1_048_576,
                capabilities=["chat", "translate", "code", "vision", "tools"],
                languages=_LANGUAGES,
                speed="fast",
                quality="great",
                notes="May experience demand spikes (503)",
            ),
            ModelInfo(
                id="gemini:gemini-3.1-flash-lite",
                provider="gemini",
                display_name="Gemini 3.1 Flash Lite",
                is_free=True,
                context_window=1_048_576,
                capabilities=["chat", "translate", "code"],
                languages=_LANGUAGES,
                speed="very_fast",
                quality="great",
                notes="Lightest, fastest, lowest cost",
            ),
        ]

    @staticmethod
    def _classify_error(exc: Exception) -> str:
        msg = (str(exc) or "").lower()
        if any(t in msg for t in ("api key", "auth", "401", "403", "permission")):
            return "invalid_key"
        return "down"

    async def health(self) -> HealthCheck:
        if not self.is_configured():
            return HealthCheck(name=self.name, status="missing_key")
        start = time.monotonic()
        try:
            await asyncio.to_thread(self._get_client().models.list)
            latency_ms = int((time.monotonic() - start) * 1000)
            return HealthCheck(name=self.name, status="ok", latency_ms=latency_ms)
        except Exception as exc:
            return HealthCheck(
                name=self.name,
                status=self._classify_error(exc),
                error=str(exc),
            )

    def _build_config(self, request: GenerationRequest) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=request.system,
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.is_configured():
            return GenerationResult(
                text="", latency_ms=0,
                model=request.model, provider=self.name,
                error="missing_key",
            )
        start = time.monotonic()
        try:
            response = await asyncio.to_thread(
                self._get_client().models.generate_content,
                model=request.model,
                contents=request.prompt,
                config=self._build_config(request),
            )
            text = response.text or ""
            latency_ms = int((time.monotonic() - start) * 1000)
            return GenerationResult(
                text=text, latency_ms=latency_ms,
                model=request.model, provider=self.name,
            )
        except Exception as exc:
            latency_ms = int((time.monotonic() - start) * 1000)
            return GenerationResult(
                text="", latency_ms=latency_ms,
                model=request.model, provider=self.name,
                error=self._classify_error(exc),
            )

    async def stream(self, request: GenerationRequest) -> AsyncIterator[GenerationChunk]:
        if not self.is_configured():
            yield GenerationChunk(delta="", done=True)
            return
        try:
            def _start_stream():
                return self._get_client().models.generate_content_stream(
                    model=request.model,
                    contents=request.prompt,
                    config=self._build_config(request),
                )
            stream = await asyncio.to_thread(_start_stream)
            for chunk in stream:
                if chunk.text:
                    yield GenerationChunk(delta=chunk.text, done=False)
            yield GenerationChunk(delta="", done=True)
        except Exception:
            yield GenerationChunk(delta="", done=True)
