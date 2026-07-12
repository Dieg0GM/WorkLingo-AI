from backend.services.translation_service import translate_text as gemini_translate
from backend.services.openai_service import openai_translate


def ai_router(request):

    if request.model == "openai":

        return openai_translate(request)


    else:

        return gemini_translate(request)