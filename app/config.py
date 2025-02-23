from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()