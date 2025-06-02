import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google AI Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "your-project-id")
    
    # Agent Configuration
    ORCHESTRATOR_MODEL = "gemini-1.5-pro"
    SUBAGENT_MODEL = "gemini-1.5-flash"
    
    # System Configuration
    MAX_ITERATIONS = 10
    TIMEOUT_SECONDS = 30
    
    # Chat Interface
    CHAT_TITLE = "Sistema Multiagente ADK"
    CHAT_DESCRIPTION = "Interfaz de chat para sistema multiagente con Google ADK"

settings = Settings()