from pathlib import Path


def build_prompt(request):

    channel = request.channel.lower()

    prompt_path = Path(__file__).parent.parent / "prompts" / f"{channel}.txt"

    with open(prompt_path, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    full_prompt = f"""
{system_prompt}

Source Language:
{request.source_language}

Target Language:
{request.target_language}

Message:

{request.text}
"""

    return full_prompt