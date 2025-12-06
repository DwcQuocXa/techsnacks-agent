"""Targeted unit tests for core nodes (with mocked I/O)."""
import asyncio
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.techsnack.graph.state import TechSnackState


async def test_news_fetcher_node_with_mocks():
    from src.techsnack.graph.nodes.news_fetcher_node import news_fetcher_node
    
    async def fake_fetch_newsapi(*_, **__):
        return [
            SimpleNamespace(
                title="OpenAI ships GPT-5.1",
                source="TechCrunch",
                summary="Major release aimed at developers.",
                url="https://example.com/openai",
            ),
            SimpleNamespace(
                title="New AI code review assistant",
                source="GitHub Blog",
                summary="Copilot now reviews PRs automatically.",
                url="https://example.com/github",
            ),
        ]
    
    async def fake_perplexity_search(_prompt: str):
        return {
            "answer": '{"today_topics":[{"topic":"GPT-5.1 launch","reason":"Most impactful developer news","fame_score":9.5,"sources":["https://example.com/openai"]}]}',
            "sources": [],
        }
    
    with patch(
        "src.techsnack.graph.nodes.news_fetcher_node.fetch_newsapi",
        side_effect=fake_fetch_newsapi,
    ), patch(
        "src.techsnack.graph.nodes.news_fetcher_node.perplexity_search",
        side_effect=fake_perplexity_search,
    ):
        state = TechSnackState(mode="auto", started_at=datetime.now())
        result = await news_fetcher_node(state)
        assert result.today_topics, "today_topics should be populated"
        assert result.today_topics[0]["topic"] == "GPT-5.1 launch"
        print("✓ news_fetcher_node: mocked topics generated")


async def test_planner_node_with_mocks():
    from src.techsnack.graph.nodes.planner_node import planner_node
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    async def fake_ainvoke(self, *_, **__):  # pylint: disable=unused-argument
        return SimpleNamespace(content='{"topic":"Refined GPT-5","search_queries":["gpt-5 developer changes","openai gpt-5 api pricing"]}')
    
    with patch.object(ChatGoogleGenerativeAI, "ainvoke", new=fake_ainvoke):
        state = TechSnackState(mode="auto", selected_topic="GPT-5.1 launch")
        result = await planner_node(state)
        assert result.plan_topic == "Refined GPT-5.1"
        assert len(result.plan_search_queries) == 2
        print("✓ planner_node: produced plan_topic + queries")


async def test_researcher_node_with_mocks():
    from src.techsnack.graph.nodes.researcher_node import researcher_node
    
    async def fake_unified_search(query: str, **_):
        return {
            "combined_sources": [
                {"title": f"Article for {query}", "snippet": "Detailed snippet", "source_engine": "Tavily"}
            ],
            "synthesized_context": f"Context for {query}",
        }
    
    with patch(
        "src.techsnack.graph.nodes.researcher_node.unified_search",
        side_effect=fake_unified_search,
    ):
        state = TechSnackState(
            mode="auto",
            plan_topic="GPT-5.1 launch",
            plan_search_queries=["gpt-5 api", "gpt-5 pricing"],
        )
        result = await researcher_node(state)
        assert result.research_data is not None
        assert len(result.research_data.sources) == 2
        print("✓ researcher_node: aggregated sources from planner queries")


async def main():
    print("=== Node Unit Tests (mocked I/O) ===\n")
    await test_news_fetcher_node_with_mocks()
    await test_planner_node_with_mocks()
    await test_researcher_node_with_mocks()
    print("\n✓ Mocked node tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

