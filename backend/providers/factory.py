from backend.config.settings import settings
from backend.providers.deepseek import DeepSeekProvider
from backend.providers.gemini import GeminiProvider
from backend.providers.groq import GroqProvider
from backend.providers.kimi import KimiProvider
from backend.providers.ollama import OllamaProvider
from backend.providers.openrouter import OpenRouterProvider
from backend.providers.registry import registry


def register_providers() -> None:
    if settings.gemini_api_key:
        registry.register(GeminiProvider(api_key=settings.gemini_api_key))
    if settings.openrouter_api_key:
        registry.register(OpenRouterProvider(api_key=settings.openrouter_api_key))
    if settings.groq_api_key:
        registry.register(GroqProvider(api_key=settings.groq_api_key))
    if settings.deepseek_api_key:
        registry.register(DeepSeekProvider(api_key=settings.deepseek_api_key))
    if settings.moonshot_api_key:
        registry.register(KimiProvider(api_key=settings.moonshot_api_key))
    registry.register(OllamaProvider.from_settings())
