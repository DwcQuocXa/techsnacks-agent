from langchain_perplexity import ChatPerplexity
from langchain_core.messages import HumanMessage
from src.techsnack.config import settings
from ..logging_config import get_logger

logger = get_logger(__name__)

async def perplexity_search(query: str) -> dict:
    """
    Search using Perplexity with smart, contextual queries.
    """
    chat = ChatPerplexity(
        model=settings.perplexity_model,
        temperature=0.3,
        api_key=settings.perplexity_api_key,
    )
    
    try:
        query_preview = query[:200] + "..." if len(query) > 200 else query
        logger.info(f"  📤 Perplexity payload: model={settings.perplexity_model}, query_length={len(query)}")
        logger.debug(f"  📤 Perplexity query: {query_preview}")
        
        response = await chat.ainvoke([HumanMessage(content=query)])
        
        sources = []
        if hasattr(response, 'response_metadata'):
            citations = response.response_metadata.get('citations', [])
            sources = [
                {
                    "url": citation,
                    "title": f"Perplexity Source {i+1}",
                    "snippet": "",
                    "source_engine": "Perplexity"
                }
                for i, citation in enumerate(citations)
            ]
        
        answer_length = len(response.content) if response.content else 0
        logger.info(f"  ✓ Perplexity: {len(sources)} citations, {answer_length} chars")
        
        return {
            "answer": response.content,
            "sources": sources,
            "raw_content": response.content
        }
    
    except Exception as e:
        logger.warning(f"  ✗ Perplexity error: {e}")
        return {
            "answer": "",
            "sources": [],
            "raw_content": ""
        }

