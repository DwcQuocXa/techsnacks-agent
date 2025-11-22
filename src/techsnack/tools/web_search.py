from tavily import TavilyClient
from src.techsnack.config import settings

async def tavily_search(query: str, max_results: int = 5, include_domains: list[str] = None):
    client = TavilyClient(api_key=settings.tavily_api_key)
    
    try:
        search_params = {
            "query": query,
            "max_results": max_results,
            "include_raw_content": False
        }
        
        if include_domains:
            search_params["include_domains"] = include_domains
        
        response = client.search(**search_params)
        
        return [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")
            }
            for result in response.get("results", [])
        ]
    except Exception as e:
        print(f"Tavily search error: {e}")
        return []

