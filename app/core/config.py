from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Iconic IcoBot Backend"
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    # AI
    GEMINI_API_KEY: str
    GROQ_API_KEY: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
