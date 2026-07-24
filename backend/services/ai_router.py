from backend.services.translation_service import translate_text as gemini_translate


def ai_router(request):
    return gemini_translate(request)