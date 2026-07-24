from backend.models.generation import GenerationRequest
from backend.models.request import TranslationRequest
from backend.models.response import TranslationResponse
from backend.providers.registry import registry


def _build_simple_prompt(request: TranslationRequest) -> str:
    return (
        f"Channel: {request.channel}\n"
        f"Tone: {request.tone}\n"
        f"Mode: {request.mode}\n"
        f"Source: {request.source_language}\n"
        f"Target: {request.target_language}\n\n"
        f"{request.text}"
    )


def _strip_provider(model_id: str) -> str:
    return model_id.split(":", 1)[1] if ":" in model_id else model_id


async def ai_router(request: TranslationRequest) -> TranslationResponse:
    provider = registry.find_for_model(request.model)
    if provider is None:
        return TranslationResponse(
            model=request.model,
            provider="unknown",
            translated="",
            latency_ms=0,
            error=f"unknown provider in model: {request.model}",
        )
    if not provider.is_configured():
        return TranslationResponse(
            model=request.model,
            provider=provider.name,
            translated="",
            latency_ms=0,
            error="missing_key",
        )

    gen_request = GenerationRequest(
        model=_strip_provider(request.model),
        prompt=_build_simple_prompt(request),
        temperature=0.3 if request.mode == "translate" else 0.7,
    )
    result = await provider.generate(gen_request)
    return TranslationResponse(
        model=request.model,
        provider=result.provider,
        translated=result.text,
        latency_ms=result.latency_ms,
        error=result.error,
    )
