import asyncio
from tavily import TavilyClient
from src.techsnack.config import settings
from .perplexity_search import perplexity_search
from .query_builder import build_quick_lookup_query
from ..logging_config import get_logger

logger = get_logger(__name__)

async def tavily_search(query: str, max_results: int = 10, include_domains: list[str] = None):
    client = TavilyClient(api_key=settings.tavily_api_key)

    try:
        # Log warning if query is suspiciously short or malformed
        if len(query) < 10:
            logger.warning(f"  ⚠️ Suspiciously short Tavily query ({len(query)} chars): '{query}'")
        if query.startswith("}") or query.startswith("{"):
            logger.warning(f"  ⚠️ Malformed Tavily query starts with bracket: '{query[:50]}'")

        search_params = {
            "query": query,
            "max_results": max_results,
            "include_raw_content": False
        }

        if include_domains:
            search_params["include_domains"] = include_domains

        logger.info(f"  📤 Tavily payload: query='{query}' ({len(query)} chars), max_results={max_results}")
        
        response = client.search(**search_params)
        results = [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")
            }
            for result in response.get("results", [])
        ]
        logger.info(
            "  ✓ Tavily: %s results (preview: %s)",
            len(results),
            "; ".join(r.get("title", "Untitled") for r in results[:3]) or "n/a",
        )
        return results
    except Exception as e:
        logger.warning(f"  ✗ Tavily search error: {e}")
        return []

async def unified_search(query: str, max_results: int = 5, include_domains: list[str] = None) -> dict:
    """
    Run both Perplexity (deep research) and Tavily (quick lookup) in parallel.
    """
    perplexity_task = perplexity_search(query)
    
    topic_for_tavily = query.split("**Topic:**")[-1].split("**")[0].strip() if "**Topic:**" in query else query[:100]
    tavily_query = build_quick_lookup_query(topic_for_tavily)
    
    tavily_task = tavily_search(
        tavily_query, 
        max_results, 
        include_domains
    )
    
    perplexity_result, tavily_result = await asyncio.gather(
        perplexity_task,
        tavily_task,
        return_exceptions=True
    )
    
    combined_sources = []
    context_parts = []
    
    if isinstance(perplexity_result, dict) and perplexity_result.get("answer"):
        combined_sources.extend(perplexity_result.get("sources", []))
        context_parts.append(f"=== Deep Research (Perplexity) ===\n{perplexity_result['answer']}")
        logger.info("  🔍 Perplexity context added (%s chars)", len(perplexity_result["answer"]))
    
    if isinstance(tavily_result, list):
        for item in tavily_result:
            combined_sources.append({
                **item,
                "source_engine": "Tavily"
            })
        
        snippets = "\n".join([
            f"• {item.get('title', 'Untitled')}: {item.get('snippet', '')}"
            for item in tavily_result[:5]
        ])
        context_parts.append(f"=== Additional Context (Tavily) ===\n{snippets}")
        logger.info("  🌐 Tavily context added (%s items)", len(tavily_result))
    
    logger.info("  📦 Unified search produced %s combined sources", len(combined_sources))
    
    return {
        "perplexity": perplexity_result if isinstance(perplexity_result, dict) else None,
        "tavily": tavily_result if isinstance(tavily_result, list) else None,
        "combined_sources": combined_sources,
        "synthesized_context": "\n\n".join(context_parts)
    }
