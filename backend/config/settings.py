from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

# Leer la API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")