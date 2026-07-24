from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    log_level: Literal["debug", "info", "warning", "error"] = "info"

    gemini_api_key: str = ""
    openrouter_api_key: str = ""
    groq_api_key: str = ""
    deepseek_api_key: str = ""
    moonshot_api_key: str = ""

    ollama_base_url: str = "http://localhost:11434"
    ollama_models: str = "qwen3:8b,llama3.3,gemma3:27b"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def configured_providers(self) -> dict[str, bool]:
        return {
            "gemini": bool(self.gemini_api_key),
            "openrouter": bool(self.openrouter_api_key),
            "groq": bool(self.groq_api_key),
            "deepseek": bool(self.deepseek_api_key),
            "kimi": bool(self.moonshot_api_key),
            "ollama": True,
        }


settings = Settings()
