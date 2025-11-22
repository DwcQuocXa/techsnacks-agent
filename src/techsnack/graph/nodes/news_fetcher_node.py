import asyncio
from datetime import datetime, timedelta

from ..state import TechSnackState
from ...tools.news_fetcher import (
    fetch_newsapi,
    fetch_hackernews,
    fetch_google_news_rss,
)

async def news_fetcher_node(state: TechSnackState) -> TechSnackState:
    results = await asyncio.gather(
        fetch_newsapi(
            query="AI OR machine learning OR developer tools",
            from_date=(datetime.now() - timedelta(days=1)),
        ),
        fetch_hackernews(limit=20),
        fetch_google_news_rss(query="technology AI"),
        return_exceptions=True
    )
    
    all_news = []
    for result in results:
        if isinstance(result, list):
            all_news.extend(result)
    
    state.raw_news = all_news
    return state

