"""Test external tool integrations."""
import asyncio

async def test_newsapi():
    from src.techsnack.tools.news_fetcher import fetch_newsapi
    from datetime import datetime, timedelta
    
    try:
        results = await fetch_newsapi("AI", datetime.now() - timedelta(days=1))
        print(f"✓ NewsAPI: fetched {len(results)} items")
        return True
    except Exception as e:
        print(f"✗ NewsAPI failed: {e}")
        return False

async def test_hackernews():
    from src.techsnack.tools.news_fetcher import fetch_hackernews
    
    try:
        results = await fetch_hackernews(5)
        print(f"✓ HackerNews: fetched {len(results)} items")
        return True
    except Exception as e:
        print(f"✗ HackerNews failed: {e}")
        return False

async def test_tavily():
    from src.techsnack.tools.web_search import tavily_search
    
    try:
        results = await tavily_search("Python programming", max_results=3)
        print(f"✓ Tavily: fetched {len(results)} results")
        return True
    except Exception as e:
        print(f"✗ Tavily failed: {e}")
        return False

async def main():
    print("=== Phase 3 Tools Verification ===\n")
    results = await asyncio.gather(
        test_newsapi(),
        test_hackernews(),
        test_tavily(),
    )
    if all(results):
        print("\n✓ All tools working!")
    else:
        print("\n✗ Some tools failed - check API keys")

if __name__ == "__main__":
    asyncio.run(main())

