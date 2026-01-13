from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required API keys
    gemini_api_key: str
    perplexity_api_key: str
    
    # Optional API keys (features will be disabled if not provided)
    newsapi_key: str | None = None
    tavily_api_key: str | None = None
    openai_api_key: str | None = None
    
    output_dir: str = "outputs"
    max_news_items: int = 30
    research_depth: int = 5
    research_concurrency: int = 3
    
    gemini_model: str = "gemini-3-flash-preview"
    gemini_temperature: float = 0.7
    perplexity_model: str = "sonar"
    openai_model: str = "gpt-5"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

