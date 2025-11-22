"""Test Perplexity integration with enhanced queries."""
import asyncio

async def test_news_discovery():
    from src.techsnack.tools.perplexity_search import perplexity_search
    from src.techsnack.tools.query_builder import build_news_discovery_query
    
    query = build_news_discovery_query()
    print(f"Query:\n{query[:200]}...\n")
    
    result = await perplexity_search(query)
    print(f"✓ News discovery: {len(result['answer'])} chars")
    print(f"  Sources: {len(result['sources'])}")
    if result['answer']:
        print(f"\n  Preview:\n  {result['answer'][:300]}...")

async def test_topic_research():
    from src.techsnack.tools.web_search import unified_search
    from src.techsnack.tools.query_builder import build_topic_research_query
    
    topic = "Vector databases for AI applications"
    query = build_topic_research_query(topic)
    
    result = await unified_search(query)
    print(f"\n✓ Topic research complete")
    print(f"  Perplexity: {bool(result['perplexity'])}")
    print(f"  Tavily: {bool(result['tavily'])}")
    print(f"  Total sources: {len(result['combined_sources'])}")

async def main():
    print("=== Perplexity Integration Test ===\n")
    await test_news_discovery()
    await test_topic_research()
    print("\n✓ All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())

