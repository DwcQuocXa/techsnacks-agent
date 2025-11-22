from ...tools.web_search import unified_search
from ...tools.query_builder import build_topic_research_query
from ..state import TechSnackState, ResearchData
from ...config import settings

async def researcher_node(state: TechSnackState) -> TechSnackState:
    """
    Deep research using enhanced queries with both search engines.
    """
    topic = state.selected_topic or state.user_topic
    
    research_query = build_topic_research_query(topic)
    
    search_results = await unified_search(
        query=research_query,
        max_results=settings.research_depth,
        include_domains=["github.com", "techcrunch.com", "medium.com", "dev.to", "arxiv.org"]
    )
    
    research = ResearchData(
        topic=topic,
        sources=search_results.get("combined_sources", []),
        key_facts=[
            src.get("snippet", "")[:300] 
            for src in search_results.get("combined_sources", []) 
            if src.get("snippet")
        ][:10],
        technical_details=search_results.get("perplexity", {}).get("answer", ""),
        context=search_results.get("synthesized_context", "")
    )
    
    state.research_data = research
    return state

