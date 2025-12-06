from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    newsapi_key: str
    tavily_api_key: str
    perplexity_api_key: str
    openai_api_key: str
    
    output_dir: str = "outputs"
    max_news_items: int = 30
    research_depth: int = 5
    research_concurrency: int = 3
    
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_temperature: float = 0.7
    perplexity_model: str = "sonar"
    openai_model: str = "gpt-5"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

