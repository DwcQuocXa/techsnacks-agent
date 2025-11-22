import aiohttp
import feedparser
from datetime import datetime
from src.techsnack.models import NewsItem
from src.techsnack.config import settings

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
                return []
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []

async def fetch_hackernews(limit: int = 20) -> list[NewsItem]:
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/topstories.json") as response:
                story_ids = await response.json()
            
            stories = []
            for story_id in story_ids[:limit]:
                async with session.get(f"{base_url}/item/{story_id}.json") as response:
                    story = await response.json()
                    if story and story.get("title"):
                        stories.append(
                            NewsItem(
                                title=story["title"],
                                url=story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                                source="HackerNews",
                                published_at=datetime.fromtimestamp(story["time"]).isoformat(),
                                summary=""
                            )
                        )
            return stories
    except Exception as e:
        print(f"HackerNews error: {e}")
        return []

async def fetch_google_news_rss(query: str) -> list[NewsItem]:
    url = f"https://news.google.com/rss/search?q={query}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        
        feed = feedparser.parse(content)
        return [
            NewsItem(
                title=entry.title,
                url=entry.link,
                source="Google News",
                published_at=entry.get("published", datetime.now().isoformat()),
                summary=entry.get("summary", "")
            )
            for entry in feed.entries[:15]
        ]
    except Exception as e:
        print(f"Google News RSS error: {e}")
        return []

