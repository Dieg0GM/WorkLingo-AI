from typing import ClassVar

from backend.models.provider import ModelInfo
from backend.providers.openai_compatible import OpenAICompatibleProvider


_KIMI_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="kimi:kimi-k3",
        provider="kimi",
        display_name="Kimi K3",
        is_free=False,
        context_window=1_048_576,
        capabilities=["chat", "translate", "code", "vision", "tools"],
        languages=["zh", "en", "ja", "ko", "es", "fr", "de", "it", "pt", "ru"],
        speed="medium",
        quality="excellent",
        notes="Moonshot flagship, 1M context. Best in Chinese. Free trial credits.",
    ),
    ModelInfo(
        id="kimi:kimi-k2.6",
        provider="kimi",
        display_name="Kimi K2.6",
        is_free=False,
        context_window=262_144,
        capabilities=["chat", "translate", "code", "vision", "tools"],
        languages=["zh", "en", "ja", "ko", "es", "fr", "de", "it", "pt", "ru"],
        speed="fast",
        quality="great",
        notes="General-purpose, strong in Chinese/English. Free trial credits.",
    ),
]


class KimiProvider(OpenAICompatibleProvider):
    name: ClassVar[str] = "kimi"
    display_name: ClassVar[str] = "Kimi (Moonshot)"
    requires_key: ClassVar[bool] = True
    is_free: ClassVar[bool] = False

    def __init__(self, api_key: str) -> None:
        super().__init__(
            name=self.name,
            display_name=self.display_name,
            base_url="https://api.moonshot.ai/v1",
            api_key=api_key,
            models=list(_KIMI_MODELS),
            is_free=self.is_free,
        )
