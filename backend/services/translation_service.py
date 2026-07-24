from google import genai

from backend.config.settings import settings
from backend.services.prompt_builder import build_prompt


client = genai.Client(api_key=settings.gemini_api_key)


from google.genai.errors import ClientError


def translate_text(request):

    
    if request.mode == "assistant":

        prompt = f"""

You are an AI communication assistant.

The user wants to create a professional message.

First improve the user's idea.
Make it natural and clear.

Then translate it into {request.target_language}.

Context:
Channel: {request.channel}
Tone: {request.tone}

User message:

{request.text}

"""


    else:

        prompt = f"""

Translate the following message.

Source language:
{request.source_language}

Target language:
{request.target_language}

Channel:
{request.channel}

Tone:
{request.tone}

Keep the original meaning.

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