from datetime import datetime, timedelta

from ..state import TechSnackState
from ...tools.news_fetcher import fetch_newsapi
from ...logging_config import get_logger

logger = get_logger(__name__)

async def news_fetcher_node(state: TechSnackState) -> TechSnackState:
    logger.info("📰 Fetching tech news from NewsAPI...")
    
    news_items = await fetch_newsapi(
        query="AI OR machine learning OR developer tools",
        from_date=(datetime.now() - timedelta(days=1)),
    )
    
    state.raw_news = news_items
    logger.info(f"✓ Fetched {len(news_items)} news items from NewsAPI")
    return state

