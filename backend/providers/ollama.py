from typing import ClassVar

from backend.config.settings import settings
from backend.models.provider import ModelInfo
from backend.providers.openai_compatible import OpenAICompatibleProvider


_DEFAULT_OLLAMA_LANGUAGES = [
    "en", "es", "ja", "fr", "de", "it", "pt", "zh", "ko", "ru",
    "ar", "hi", "nl", "sv", "pl", "tr", "vi", "th", "id", "uk",
]


def _build_ollama_models(model_names: list[str]) -> list[ModelInfo]:
    result = []
    for name in model_names:
        name = name.strip()
        if not name:
            continue
        n = name.lower()
        if any(tag in n for tag in ("coder", "code", "math")):
            caps = ["chat", "code"]
            quality = "good"
            speed = "medium"
        elif "vision" in n or "vl" in n:
            caps = ["chat", "translate", "vision"]
            quality = "great"
            speed = "medium"
        elif "lite" in n or "small" in n or "mini" in n or "1b" in n or "3b" in n or "nano" in n:
            caps = ["chat", "translate"]
            quality = "good"
            speed = "very_fast"
        elif "27b" in n or "32b" in n or "70b" in n or "72b" in n or "480b" in n:
            caps = ["chat", "translate", "code", "tools"]
            quality = "great"
            speed = "slow"
        else:
            caps = ["chat", "translate", "code"]
            quality = "great"
            speed = "fast"
        result.append(
            ModelInfo(
                id=f"ollama:{name}",
                provider="ollama",
                display_name=f"Ollama {name}",
                is_free=True,
                context_window=32_768,
                capabilities=caps,
                languages=list(_DEFAULT_OLLAMA_LANGUAGES),
                speed=speed,
                quality=quality,
                notes="Local, requires `ollama pull <model>`",
            )
        )
    return result


class OllamaProvider(OpenAICompatibleProvider):
    name: ClassVar[str] = "ollama"
    display_name: ClassVar[str] = "Ollama (local)"
    requires_key: ClassVar[bool] = False
    is_free: ClassVar[bool] = True

    def __init__(self, base_url: str, model_names: list[str]) -> None:
        super().__init__(
            name=self.name,
            display_name=self.display_name,
            base_url=base_url,
            api_key="",
            models=_build_ollama_models(model_names),
            is_free=self.is_free,
            requires_key=False,
        )

    @staticmethod
    def from_settings() -> "OllamaProvider":
        names = [n for n in settings.ollama_models.split(",") if n.strip()]
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model_names=names,
        )
