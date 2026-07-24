# Reglas del proyecto

## Objetivo

WorkLingo AI es un asistente profesional de comunicación multilingüe
para uso individual y corporativo. Primera fase: traductor y reescritor
de mensajes con selección de proveedor de IA.

## Stack

- Python 3.11+ (probado en 3.14)
- FastAPI + Uvicorn (ASGI)
- Pydantic v2 (DTOs) + pydantic-settings (config)
- google-genai 2.14.0 (Gemini)
- OpenCode Go (proxy OpenAI/Anthropic compatible)
- python-dotenv (variables de entorno)

## Estructura

- `backend/main.py` — entrypoint FastAPI, rutas estáticas, endpoints
- `backend/models/` — DTOs Pydantic
- `backend/providers/` — adaptadores de IA por proveedor (Fase 0b)
- `backend/services/` — lógica de aplicación y router
- `backend/prompts/` — plantillas de prompt por canal
- `frontend/` — HTML/CSS/JS estático servido por FastAPI en dev
- `tests/` — tests pytest (Fase 1)
- `docs/` — documentación (Fase 1)

## Providers de IA soportados (Fase 0)

- **Gemini** directo (`models/gemini-3.5-flash`) — clave en `GEMINI_API_KEY`
- **OpenCode Go** (proxy con catálogo curado) — clave en `OPENCODE_GO_API_KEY`

Añadir un provider nuevo = crear `backend/providers/<nombre>.py` + 1 import
en `backend/providers/__init__.py`. Cero cambios en router, main ni frontend.

## Reglas de contribución

- No commitear secretos. Las claves viven sólo en `.env` (gitignored).
- No usar Flask, SQLite ni Docker en este proyecto (decidido).
- No añadir OpenAI hasta que se decida explícitamente.
- Commits pequeños y verificables. Un commit por cambio lógico.
- Cero código muerto. Si no se usa, se borra.
- Pydantic `Literal` para enums. `max_length` para strings largos.
- Toda ruta de error devuelve `HTTPException` con código correcto.
- Provider/modelo en URL como `provider:model` (ej. `gemini:gemini-3.5-flash`).
