import aiohttp
import logging
from datetime import datetime
from src.techsnack.models import NewsItem
from src.techsnack.config import settings

logger = logging.getLogger(__name__)

async def fetch_newsapi(query: str, from_date: datetime) -> list[NewsItem]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date.strftime("%Y-%m-%d"),
        "sortBy": "publishedAt",
        "apiKey": settings.newsapi_key,
        "pageSize": 30,
        "language": "en"
    }
    
    logger.info(f"  📤 NewsAPI payload: query='{query}', from={from_date.strftime('%Y-%m-%d')}, pageSize=30")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("articles", [])
                    return [
                        NewsItem(
                            title=article["title"],
                            url=article["url"],
                            source=article["source"]["name"],
                            published_at=article["publishedAt"],
                            summary=article.get("description", "")
                        )
                        for article in articles if article.get("title")
                    ]
                logger.warning(f"  ✗ NewsAPI error: HTTP {response.status}")
                return []
    except Exception as e:
        logger.warning(f"  ✗ NewsAPI error: {e}")
        return []

