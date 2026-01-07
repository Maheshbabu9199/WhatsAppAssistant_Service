from enum import Enum


class LLMProviders(Enum):
    OPENAI = "openai"
    GROQ = "groq"


class PromptNames(Enum):
    WHATSAPP_SERVICE_CHAT_PROMPT = "WhatsApp_Service_System_Prompt"
