from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    max_tokens: int = 500
    temperature: float = 0.7
    ai_model: str ="deepseek-r1-distill-llama-70b"
    ai_model_provider: str = "groq"
    astra_db_token: str
    astra_db_id: str
    astra_db_secret: str
    astra_db_client_id:str
    astra_db_region: str


    class Config:
        env_file = ".env"

settings = Settings()