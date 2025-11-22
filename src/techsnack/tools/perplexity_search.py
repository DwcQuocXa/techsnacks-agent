from langchain_community.chat_models import ChatPerplexity
from langchain_core.messages import HumanMessage
from src.techsnack.config import settings

async def perplexity_search(query: str) -> dict:
    """
    Search using Perplexity with smart, contextual queries.
    """
    chat = ChatPerplexity(
        model=settings.perplexity_model,
        temperature=0.3,
        pplx_api_key=settings.perplexity_api_key,
        return_citations=True,
        return_related_questions=False
    )
    
    try:
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
        
        return {
            "answer": response.content,
            "sources": sources,
            "raw_content": response.content
        }
    
    except Exception as e:
        print(f"Perplexity error: {e}")
        return {
            "answer": "",
            "sources": [],
            "raw_content": ""
        }

