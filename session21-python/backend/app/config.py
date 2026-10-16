from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MentorSync API"
    environment: str = "production"
    database_url: str = "postgresql+psycopg://mentorsync:mentorsync@localhost:5432/mentorsync"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
