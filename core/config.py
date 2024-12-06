from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  app_name: str = "SageAI API"
  app_version: str = "1.0.0"
  app_description: str = "API for food analysis and health recommendations"
  model_name_groq: str = "llama-3.1-70b-versatile"
  model_name_openai: str = "gpt-4o-2024-08-06"
    
  class Config:
    env_file = ".env"

settings = Settings()