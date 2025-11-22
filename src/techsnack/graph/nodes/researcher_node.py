from ...tools.web_search import unified_search
from ...tools.query_builder import build_topic_research_query
from ..state import TechSnackState, ResearchData
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)

async def researcher_node(state: TechSnackState) -> TechSnackState:
    """
    Deep research using enhanced queries with both search engines.
    """
    topic = state.selected_topic or state.user_topic
    logger.info(f"🔬 Researching topic: {topic}")
    
    research_query = build_topic_research_query(topic)
    
    logger.info("  → Running Perplexity + Tavily search in parallel...")
    search_results = await unified_search(
        query=research_query,
        max_results=settings.research_depth,
        include_domains=["github.com", "techcrunch.com", "medium.com", "dev.to", "arxiv.org"]
    )
    
    combined_sources = search_results.get("combined_sources", [])
    perplexity_sources = len([s for s in combined_sources if s.get("source_engine") == "Perplexity"])
    tavily_sources = len([s for s in combined_sources if s.get("source_engine") == "Tavily"])
    
    logger.info(f"✓ Research complete: {perplexity_sources} Perplexity + {tavily_sources} Tavily = {len(combined_sources)} total sources")
    
    research = ResearchData(
        topic=topic,
        sources=combined_sources,
        key_facts=[
            src.get("snippet", "")[:300] 
            for src in combined_sources
            if src.get("snippet")
        ][:10],
        technical_details=search_results.get("perplexity", {}).get("answer", ""),
        context=search_results.get("synthesized_context", "")
    )
    
    state.research_data = research
    return state

