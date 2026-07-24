from typing import ClassVar

from backend.models.provider import ModelInfo
from backend.providers.openai_compatible import OpenAICompatibleProvider


_OPENROUTER_FREE_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="openrouter:google/gemma-4-31b-it:free",
        provider="openrouter",
        display_name="Gemma 4 31B (free)",
        is_free=True,
        context_window=262_144,
        capabilities=["chat", "translate", "code"],
        languages=["en", "es", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru", "ar", "hi", "nl", "sv", "pl", "tr", "vi", "th", "id", "uk"],
        speed="fast",
        quality="great",
        notes="Google, top free for translation",
    ),
    ModelInfo(
        id="openrouter:google/gemma-4-26b-a4b-it:free",
        provider="openrouter",
        display_name="Gemma 4 26B A4B (free)",
        is_free=True,
        context_window=262_144,
        capabilities=["chat", "translate", "code"],
        languages=["en", "es", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru", "ar", "hi", "nl", "sv", "pl", "tr", "vi", "th", "id", "uk"],
        speed="fast",
        quality="great",
        notes="Google MoE",
    ),
    ModelInfo(
        id="openrouter:nvidia/nemotron-3-super-120b-a12b:free",
        provider="openrouter",
        display_name="Nemotron 3 Super 120B (free)",
        is_free=True,
        context_window=262_144,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ru"],
        speed="medium",
        quality="great",
        notes="NVIDIA MoE, large",
    ),
    ModelInfo(
        id="openrouter:openai/gpt-oss-20b:free",
        provider="openrouter",
        display_name="GPT-OSS 20B (free)",
        is_free=True,
        context_window=131_072,
        capabilities=["chat", "translate", "code", "tools"],
        languages=["en", "es", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru"],
        speed="fast",
        quality="great",
        notes="OpenAI open-weights",
    ),
    ModelInfo(
        id="openrouter:openrouter/free",
        provider="openrouter",
        display_name="OpenRouter Free Router",
        is_free=True,
        context_window=200_000,
        capabilities=["chat", "translate"],
        languages=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"],
        speed="medium",
        quality="good",
        notes="Auto-routes to best free model at request time",
    ),
]


class OpenRouterProvider(OpenAICompatibleProvider):
    name: ClassVar[str] = "openrouter"
    display_name: ClassVar[str] = "OpenRouter"
    requires_key: ClassVar[bool] = True
    is_free: ClassVar[bool] = True

    def __init__(self, api_key: str) -> None:
        super().__init__(
            name=self.name,
            display_name=self.display_name,
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            models=list(_OPENROUTER_FREE_MODELS),
            is_free=self.is_free,
            extra_headers={
                "HTTP-Referer": "https://worklingo.ai",
                "X-Title": "WorkLingo AI",
            },
        )
