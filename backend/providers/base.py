from abc import ABC, abstractmethod
from typing import AsyncIterator, ClassVar

from backend.models.generation import GenerationChunk, GenerationRequest, GenerationResult
from backend.models.provider import HealthCheck, ModelInfo


class BaseProvider(ABC):
    name: ClassVar[str]
    display_name: ClassVar[str]
    requires_key: ClassVar[bool]
    is_free: ClassVar[bool]

    def is_configured(self) -> bool:
        return True

    @abstractmethod
    def list_models(self) -> list[ModelInfo]: ...

    @abstractmethod
    async def health(self) -> HealthCheck: ...

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResult: ...

    @abstractmethod
    def stream(self, request: GenerationRequest) -> AsyncIterator[GenerationChunk]: ...
