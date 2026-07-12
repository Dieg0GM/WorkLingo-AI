from openai import OpenAI

from backend.config.settings import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def openai_translate(request):

    prompt = f"""

You are WorkLingo AI, a professional communication assistant.

Improve the user's message and translate it.

Source language:
{request.source_language}

Target language:
{request.target_language}

Channel:
{request.channel}

Tone:
{request.tone}

Message:

{request.text}

"""


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )


    return {

        "original": request.text,

        "translated": response.output_text,

        "channel": request.channel

    }