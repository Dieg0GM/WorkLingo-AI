from backend.providers.base import BaseProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    def all(self) -> list[BaseProvider]:
        return list(self._providers.values())

    def configured(self) -> list[BaseProvider]:
        return [p for p in self._providers.values() if p.is_configured()]

    def find_for_model(self, model_id: str) -> BaseProvider | None:
        if ":" not in model_id:
            return None
        provider_name = model_id.split(":", 1)[0]
        return self.get(provider_name)


registry = ProviderRegistry()
