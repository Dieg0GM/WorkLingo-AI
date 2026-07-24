from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str
    channel: str
    tone: str
    mode: str
    model: str
