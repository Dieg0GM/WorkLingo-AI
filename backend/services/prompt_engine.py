from dataclasses import dataclass

from backend.models.request import TranslationRequest


@dataclass(frozen=True)
class Example:
    source_lang: str
    target_lang: str
    source: str
    target: str


_SYSTEM_PROMPTS: dict[str, str] = {
    "email": (
        "You are WorkLingo AI, an expert translator and cross-cultural communication "
        "assistant for professional email.\n\n"
        "Your task: translate the user's message from {source} to {target} for an email "
        "context.\n\n"
        "Rules:\n"
        "- Preserve the original meaning, intent, and any factual information exactly.\n"
        "- Adapt register, honorifics, and cultural conventions to the target language "
        "(e.g., keigo in Japanese, Sie/du in German, usted/tú in Spanish, vouvoiement in French).\n"
        "- Preserve proper nouns, brand names, URLs, code, numbers, currency, and dates exactly.\n"
        "- Match the requested tone. If no tone is given, default to neutral professional.\n"
        "- Output ONLY the translated message. No preamble, no explanation, no labels, no quotation marks."
    ),
    "slack": (
        "You are WorkLingo AI, a translator for workplace chat on Slack.\n\n"
        "Your task: translate the user's message from {source} to {target} for a Slack "
        "conversation, keeping it natural and concise.\n\n"
        "Rules:\n"
        "- Preserve the meaning and intent. Be concise — Slack favors brevity.\n"
        "- Use natural conversational register in the target language.\n"
        "- Preserve emoji, @mentions, #channels, code blocks, links, and formatting exactly.\n"
        "- Match the requested tone. If no tone is given, default to friendly professional.\n"
        "- Output ONLY the translated message. No preamble, no explanation, no labels."
    ),
    "chat": (
        "You are WorkLingo AI, a professional translation assistant for general chat.\n\n"
        "Your task: translate the user's message from {source} to {target} for a chat context.\n\n"
        "Rules:\n"
        "- Preserve the meaning and intent.\n"
        "- Use natural conversational register in the target language.\n"
        "- Match the requested tone.\n"
        "- Output ONLY the translated message. No preamble, no explanation, no labels."
    ),
}


_EXAMPLES: dict[str, tuple[Example, ...]] = {
    "email": (
        Example(
            source_lang="en", target_lang="es",
            source="Hi John, just a quick reminder about our meeting tomorrow at 10am. Let me know if the time still works for you.",
            target="Hola John, solo un recordatorio rápido sobre nuestra reunión de mañana a las 10h. Avísame si el horario sigue siendo conveniente para ti.",
        ),
        Example(
            source_lang="en", target_lang="ja",
            source="Dear Mr. Tanaka, thank you for your prompt reply. Could you please send the signed contract by Friday?",
            target="田中様、ご迅速なご返信ありがとうございます。恐れ入りますが、金曜日までに署名済みの契約書をお送りいただけますでしょうか。",
        ),
        Example(
            source_lang="es", target_lang="en",
            source="Hola María, te escribo para confirmar la reunión del jueves. Quedo a la espera de tu confirmación.",
            target="Hi María, I'm writing to confirm Thursday's meeting. Looking forward to your confirmation.",
        ),
    ),
    "slack": (
        Example(
            source_lang="en", target_lang="es",
            source="Hey @david, the deploy failed again 😅 Can you take a look?",
            target="Oye @david, el deploy falló otra vez 😅 ¿Puedes echarle un ojo?",
        ),
        Example(
            source_lang="en", target_lang="ja",
            source="Looks good! 🎉 Thanks for the quick fix.",
            target="良さそうです！🎉 素早い対応ありがとうございます。",
        ),
        Example(
            source_lang="es", target_lang="en",
            source="Listo, ya está subido al repo.",
            target="Done, it's already pushed to the repo.",
        ),
    ),
    "chat": (
        Example(
            source_lang="en", target_lang="es",
            source="What time works for you?",
            target="¿A qué hora te viene bien?",
        ),
        Example(
            source_lang="en", target_lang="ja",
            source="See you tomorrow!",
            target="また明日！",
        ),
        Example(
            source_lang="es", target_lang="en",
            source="¿Vamos a la reunión de las 3?",
            target="Are we going to the 3pm meeting?",
        ),
    ),
}


class PromptEngine:
    def build(self, request: TranslationRequest) -> tuple[str, str]:
        return self._render_system(request), self._render_user(request)

    def _render_system(self, request: TranslationRequest) -> str:
        template = _SYSTEM_PROMPTS.get(request.channel, _SYSTEM_PROMPTS["chat"])
        return template.format(source=request.source_language, target=request.target_language)

    def _render_user(self, request: TranslationRequest) -> str:
        examples = self._select_examples(request)
        parts: list[str] = [
            f"Source language: {request.source_language}",
            f"Target language: {request.target_language}",
            f"Tone: {request.tone}",
        ]
        if examples:
            parts.append("")
            parts.append("Examples of the expected output:")
            for i, ex in enumerate(examples, 1):
                parts.append("")
                parts.append(f"Example {i}:")
                parts.append(f"  Source ({ex.source_lang}): {ex.source}")
                parts.append(f"  Target ({ex.target_lang}): {ex.target}")
        parts.append("")
        parts.append("Now translate this message:")
        parts.append(f"Source ({request.source_language}): {request.text}")
        parts.append(f"Target ({request.target_language}):")
        return "\n".join(parts)

    def _select_examples(self, request: TranslationRequest) -> tuple[Example, ...]:
        all_examples = _EXAMPLES.get(request.channel, ())
        if not all_examples:
            return ()
        exact = tuple(
            ex for ex in all_examples
            if ex.source_lang == request.source_language
            and ex.target_lang == request.target_language
        )
        if exact:
            return exact
        return all_examples
