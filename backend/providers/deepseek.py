from typing import ClassVar

from backend.models.provider import ModelInfo
from backend.providers.openai_compatible import OpenAICompatibleProvider


_DEEPSEEK_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="deepseek:deepseek-chat",
        provider="deepseek",
        display_name="DeepSeek V3 Chat",
        is_free=False,
        context_window=65_536,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "zh", "ja", "ko", "es", "fr", "de", "it", "pt", "ru", "ar"],
        speed="medium",
        quality="excellent",
        notes="671B MoE (37B active). Strong reasoning. Free credits on signup.",
    ),
    ModelInfo(
        id="deepseek:deepseek-reasoner",
        provider="deepseek",
        display_name="DeepSeek R1 Reasoner",
        is_free=False,
        context_window=65_536,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "zh", "ja", "ko", "es", "fr", "de", "it", "pt", "ru"],
        speed="slow",
        quality="excellent",
        notes="R1 reasoning model, best for complex translation. Free credits on signup.",
    ),
]


class DeepSeekProvider(OpenAICompatibleProvider):
    name: ClassVar[str] = "deepseek"
    display_name: ClassVar[str] = "DeepSeek"
    requires_key: ClassVar[bool] = True
    is_free: ClassVar[bool] = False

    def __init__(self, api_key: str) -> None:
        super().__init__(
            name=self.name,
            display_name=self.display_name,
            base_url="https://api.deepseek.com/v1",
            api_key=api_key,
            models=list(_DEEPSEEK_MODELS),
            is_free=self.is_free,
        )
