"""Graph wiring tests with mocked nodes."""
import asyncio
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState, ResearchData


async def fake_news_fetcher(state: TechSnackState) -> TechSnackState:
    state.raw_news = [SimpleNamespace(title="Mock AI News", source="MockSource", summary="Summary", url="https://example.com")]
    state.today_topics = [{"topic": "Mock Topic", "reason": "Mock reason", "fame_score": 9, "sources": ["https://example.com"]}]
    return state


async def fake_topic_selector(state: TechSnackState) -> TechSnackState:
    state.selected_topic = state.today_topics[0]["topic"]
    state.selection_reasoning = "Highest impact"
    return state


async def fake_planner(state: TechSnackState) -> TechSnackState:
    state.plan_topic = state.selected_topic or state.user_topic
    state.plan_search_queries = ["mock query 1", "mock query 2"]
    return state


async def fake_researcher(state: TechSnackState) -> TechSnackState:
    state.research_data = ResearchData(
        topic=state.plan_topic,
        sources=[{"title": "Mock Source", "snippet": "Details", "source_engine": "Tavily", "query_used": "mock query 1"}],
        key_facts=["Fact"],
        technical_details="",
        context="Mock context",
    )
    return state


async def fake_writer(state: TechSnackState) -> TechSnackState:
    state.article = f"# Mock Article\n\nTopic: {state.plan_topic}"
    state.article_metadata = {"topic": state.plan_topic, "word_count": 5}
    state.completed_at = datetime.now()
    return state


async def run_graph(mode: str, **state_kwargs):
    with patch("src.techsnack.graph.graph.news_fetcher_node", fake_news_fetcher), \
         patch("src.techsnack.graph.graph.topic_selector_node", fake_topic_selector), \
         patch("src.techsnack.graph.graph.planner_node", fake_planner), \
         patch("src.techsnack.graph.graph.researcher_node", fake_researcher), \
         patch("src.techsnack.graph.graph.writer_node", fake_writer):
        graph = create_techsnack_graph()
        initial_state = TechSnackState(mode=mode, started_at=datetime.now(), **state_kwargs)
        return await graph.ainvoke(initial_state)


async def main():
    print("=== Graph wiring tests (mocked nodes) ===\n")
    
    auto_result = await run_graph("auto")
    auto_topic = auto_result.get("selected_topic") if isinstance(auto_result, dict) else auto_result.selected_topic
    auto_article = auto_result.get("article") if isinstance(auto_result, dict) else auto_result.article
    assert auto_topic == "Mock Topic"
    assert auto_article.startswith("# Mock Article")
    print("✓ Auto mode path executed via mock nodes")
    
    manual_result = await run_graph("manual", user_topic="Manual Topic")
    manual_plan_topic = manual_result.get("plan_topic") if isinstance(manual_result, dict) else manual_result.plan_topic
    assert manual_plan_topic == "Manual Topic"
    print("✓ Manual mode path executed via mock nodes")
    
    print("\n✓ Graph wiring verified with mocks")


if __name__ == "__main__":
    asyncio.run(main())

