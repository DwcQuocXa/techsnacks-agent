from ...tools.web_search import tavily_search
from ..state import TechSnackState, ResearchData
from ...config import settings

async def researcher_node(state: TechSnackState) -> TechSnackState:
    topic = state.selected_topic or state.user_topic
    
    search_results = await tavily_search(
        query=topic,
        max_results=settings.research_depth,
        include_domains=["github.com", "techcrunch.com", "medium.com", "dev.to"]
    )
    
    research = ResearchData(
        topic=topic,
        sources=search_results,
        key_facts=[r.get("snippet", "") for r in search_results],
        context="\n\n".join([
            f"{r.get('title', '')}: {r.get('snippet', '')}"
            for r in search_results
        ])
    )
    
    state.research_data = research
    return state

