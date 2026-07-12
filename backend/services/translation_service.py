from google import genai

from backend.config.settings import GEMINI_API_KEY
from backend.services.prompt_builder import build_prompt


client = genai.Client(api_key=GEMINI_API_KEY)


from google.genai.errors import ClientError


def translate_text(request):

    print("DEBUG REQUEST:")
    print(request)
    print(request.model_dump())

    prompt = f"""
    Translate the following text.

    Source language:
    {request.source_language}

    Target language:
    {request.target_language}

    Channel:
    {request.channel}

    Tone:
    {request.tone}

    Mode:
    {request.mode}

    Text:
    {request.text}
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )


        return {

            "original": request.text,

            "translated": response.text,

            "channel": request.channel

        }


    except ClientError as e:


        return {


            "original": request.text,

            "translated": "",

            "error": "Gemini quota exceeded or unavailable"


        }