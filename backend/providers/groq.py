from typing import ClassVar

from backend.models.provider import ModelInfo
from backend.providers.openai_compatible import OpenAICompatibleProvider


_GROQ_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="groq:llama-3.1-8b-instant",
        provider="groq",
        display_name="Llama 3.1 8B Instant",
        is_free=False,
        context_window=131_072,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ru", "ar", "hi"],
        speed="very_fast",
        quality="good",
        notes="Ultra fast, low cost. Free trial credits.",
    ),
    ModelInfo(
        id="groq:openai/gpt-oss-120b",
        provider="groq",
        display_name="GPT-OSS 120B",
        is_free=False,
        context_window=131_072,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ru"],
        speed="fast",
        quality="great",
        notes="OpenAI open-weights, MoE 120B. Free trial credits.",
    ),
    ModelInfo(
        id="groq:qwen/qwen-3.6-27b",
        provider="groq",
        display_name="Qwen 3.6 27B",
        is_free=False,
        context_window=131_072,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "es", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru", "ar", "hi"],
        speed="fast",
        quality="great",
        notes="Alibaba Qwen, multilingual strong. Free trial credits.",
    ),
    ModelInfo(
        id="groq:moonshotai/kimi-k2-instruct-0905",
        provider="groq",
        display_name="Kimi K2 Instruct",
        is_free=False,
        context_window=131_072,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "zh", "ja", "ko", "es", "fr", "de"],
        speed="fast",
        quality="great",
        notes="Moonshot Kimi, strong in Chinese. Free trial credits.",
    ),
]


class GroqProvider(OpenAICompatibleProvider):
    name: ClassVar[str] = "groq"
    display_name: ClassVar[str] = "Groq"
    requires_key: ClassVar[bool] = True
    is_free: ClassVar[bool] = False

    def __init__(self, api_key: str) -> None:
        super().__init__(
            name=self.name,
            display_name=self.display_name,
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
            models=list(_GROQ_MODELS),
            is_free=self.is_free,
        )
