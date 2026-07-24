import asyncio
import time
from typing import AsyncIterator, ClassVar

from openai import AsyncOpenAI

from backend.models.generation import GenerationChunk, GenerationRequest, GenerationResult
from backend.models.provider import HealthCheck, ModelInfo
from backend.providers.base import BaseProvider


class OpenAICompatibleProvider(BaseProvider):
    requires_key: ClassVar[bool] = True

    def __init__(
        self,
        *,
        name: str,
        display_name: str,
        base_url: str,
        api_key: str,
        models: list[ModelInfo],
        is_free: bool,
        requires_key: bool = True,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.name = name
        self.display_name = display_name
        self.base_url = base_url
        self.api_key = api_key
        self._models = models
        self.is_free = is_free
        self.requires_key = requires_key
        self._extra_headers = extra_headers or {}
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self.api_key or "not-required",
                base_url=self.base_url,
                default_headers=self._extra_headers or None,
            )
        return self._client

    def is_configured(self) -> bool:
        if not self.requires_key:
            return True
        return bool(self.api_key)

    def list_models(self) -> list[ModelInfo]:
        return self._models

    def _classify_error(self, exc: Exception) -> str:
        msg = (str(exc) or "").lower()
        if any(token in msg for token in ("api key", "apikey", "unauthorized", "401", "auth")):
            return "invalid_key"
        if any(token in msg for token in ("429", "rate", "quota", "limit")):
            return "down"
        return "down"

    async def health(self) -> HealthCheck:
        if not self.is_configured():
            return HealthCheck(name=self.name, status="missing_key")
        start = time.monotonic()
        try:
            await self._get_client().models.list()
            latency_ms = int((time.monotonic() - start) * 1000)
            return HealthCheck(name=self.name, status="ok", latency_ms=latency_ms)
        except Exception as exc:
            status = self._classify_error(exc)
            return HealthCheck(name=self.name, status=status, error=str(exc))

    def _build_messages(self, request: GenerationRequest) -> list[dict]:
        messages: list[dict] = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.is_configured():
            return GenerationResult(
                text="",
                latency_ms=0,
                model=request.model,
                provider=self.name,
                error="missing_key",
            )
        start = time.monotonic()
        try:
            response = await self._get_client().chat.completions.create(
                model=request.model,
                messages=self._build_messages(request),
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
            text = (response.choices[0].message.content or "") if response.choices else ""
            latency_ms = int((time.monotonic() - start) * 1000)
            return GenerationResult(
                text=text,
                latency_ms=latency_ms,
                model=request.model,
                provider=self.name,
            )
        except Exception as exc:
            latency_ms = int((time.monotonic() - start) * 1000)
            return GenerationResult(
                text="",
                latency_ms=latency_ms,
                model=request.model,
                provider=self.name,
                error=self._classify_error(exc),
            )

    async def stream(self, request: GenerationRequest) -> AsyncIterator[GenerationChunk]:
        if not self.is_configured():
            yield GenerationChunk(delta="", done=True)
            return
        try:
            stream = await self._get_client().chat.completions.create(
                model=request.model,
                messages=self._build_messages(request),
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    yield GenerationChunk(delta=delta, done=False)
            yield GenerationChunk(delta="", done=True)
        except Exception:
            yield GenerationChunk(delta="", done=True)
