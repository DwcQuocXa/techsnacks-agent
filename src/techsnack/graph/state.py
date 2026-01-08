from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ResearchData(BaseModel):
    topic: str
    sources: list[dict[str, Any]] = []
    key_facts: list[str] = []
    technical_details: str = ""
    context: str = ""

class TechSnackState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    mode: str
    user_topic: str | None = None
    user_query: str | None = None
    writer_model: str = "gemini-3-flash-preview"
    raw_news: list = []
    today_topics: list[dict[str, Any]] = Field(default_factory=list)
    selected_topic: str | None = None
    selection_reasoning: str | None = None
    plan_topic: str | None = None
    plan_search_queries: list[str] = Field(default_factory=list)
    research_data: ResearchData | None = None
    article: str | None = None
    article_metadata: dict[str, Any] = {}
    started_at: datetime | None = None
    completed_at: datetime | None = None

