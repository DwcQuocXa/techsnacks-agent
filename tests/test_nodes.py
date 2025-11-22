"""Test each node independently."""
import asyncio
from datetime import datetime
from src.techsnack.graph.state import TechSnackState

async def test_news_fetcher_node():
    from src.techsnack.graph.nodes.news_fetcher_node import news_fetcher_node
    
    state = TechSnackState(mode="auto", started_at=datetime.now())
    result = await news_fetcher_node(state)
    print(f"✓ News Fetcher: {len(result.raw_news)} items")
    return result

async def test_researcher_node():
    from src.techsnack.graph.nodes.researcher_node import researcher_node
    
    state = TechSnackState(mode="manual", user_topic="Python async programming")
    result = await researcher_node(state)
    print(f"✓ Researcher: {len(result.research_data.sources)} sources")
    return result

async def main():
    print("=== Phase 5 Nodes Verification ===\n")
    await test_news_fetcher_node()
    await test_researcher_node()
    print("\n✓ Nodes working!")

if __name__ == "__main__":
    asyncio.run(main())

