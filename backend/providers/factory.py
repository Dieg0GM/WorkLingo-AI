from backend.config.settings import settings
from backend.providers.gemini import GeminiProvider
from backend.providers.registry import registry


def register_providers() -> None:
    if settings.gemini_api_key:
        registry.register(GeminiProvider(api_key=settings.gemini_api_key))
