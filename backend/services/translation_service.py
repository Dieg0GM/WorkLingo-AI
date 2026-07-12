from google import genai

from backend.config.settings import GEMINI_API_KEY
from backend.services.prompt_builder import build_prompt


client = genai.Client(api_key=GEMINI_API_KEY)


def translate_text(request):

    prompt = build_prompt(request)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return {
        "original": request.text,
        "translated": response.text,
        "channel": request.channel,
    }