import asyncio

from ...tools.web_search import unified_search
from ..state import TechSnackState, ResearchData
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)

async def researcher_node(state: TechSnackState) -> TechSnackState:
    """
    Deep research using planner-generated queries across Perplexity + Tavily.
    """
    topic = state.plan_topic or state.selected_topic or state.user_topic
    queries = state.plan_search_queries or ([topic] if topic else [])
    
    if not topic:
        logger.warning("⚠️ Research skipped: no topic available")
        state.research_data = None
        return state
    
    logger.info(f"🔬 Researching topic: {topic}")
    logger.info(f"  → Executing {len(queries)} search queries (concurrency={settings.research_concurrency})")
    
    combined_sources: list[dict] = []
    contexts: list[str] = []
    
    semaphore = asyncio.Semaphore(max(1, settings.research_concurrency))
    
    async def run_query(query: str):
        async with semaphore:
            result = await unified_search(
                query=query,
                max_results=settings.research_depth,
                # No domain filtering - let search engines return their best results
            )
            return query, result
    
    tasks = [asyncio.create_task(run_query(query)) for query in queries]
    
    for task in asyncio.as_completed(tasks):
        query, result = await task
        sources_before = len(result.get("combined_sources", []))
        sources = result.get("combined_sources", [])
        for src in sources:
            src["query_used"] = query
        combined_sources.extend(sources)
        
        snippet = result.get("synthesized_context")
        if snippet:
            contexts.append(snippet)
            logger.info("    🧾 Full context for '%s':\n%s", query, snippet)
        
        logger.info(
            "    ↳ Query '%s' returned %s sources; context snippet length=%s",
            query,
            sources_before,
            len(snippet or ""),
        )
    
    research = ResearchData(
        topic=topic,
        sources=combined_sources,
        key_facts=[
            src.get("snippet", "")[:300]
            for src in combined_sources
            if src.get("snippet")
        ][:10],
        technical_details="",
        context="\n\n".join(contexts),
    )
    
    top_sources_preview = [
        f"{src.get('source_engine','?')} | {src.get('title','(untitled)')}"
        for src in combined_sources[:5]
    ]
    combined_context = "\n\n".join(contexts)
    logger.info(
        "✓ Research complete with %s sources (preview: %s)",
        len(combined_sources),
        "; ".join(top_sources_preview) or "n/a",
    )
    logger.info("  📚 Combined research context:\n%s", combined_context or "<empty>")
    state.research_data = research
    return state

