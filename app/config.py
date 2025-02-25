from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    max_tokens: int = 500
    temperature: float = 0.7
    ai_model: str ="deepseek-r1-distill-llama-70b"
    ai_model_provider: str = "groq"

    class Config:
        env_file = ".env"

settings = Settings()