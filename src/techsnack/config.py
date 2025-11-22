from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    newsapi_key: str
    tavily_api_key: str
    
    output_dir: str = "outputs"
    max_news_items: int = 30
    research_depth: int = 5
    
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

