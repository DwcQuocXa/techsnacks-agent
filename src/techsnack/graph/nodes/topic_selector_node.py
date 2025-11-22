import json
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts.prompts import get_topic_selector_prompt
from ...tools.perplexity_search import perplexity_search
from ...tools.query_builder import build_news_discovery_query
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)

async def topic_selector_node(state: TechSnackState) -> TechSnackState:
    """
    Use Perplexity for news discovery, then LLM for topic selection.
    """
    logger.info("🔍 Discovering today's trending tech news...")
    news_discovery = await perplexity_search(build_news_discovery_query())
    logger.info(f"✓ Found {len(news_discovery.get('sources', []))} Perplexity sources")
    
    logger.info("🎯 Selecting best topic for TechSnack...")
    news_summary = f"=== Today's Trending Tech News (Perplexity) ===\n{news_discovery.get('answer', '')}\n\n"
    news_summary += "=== Headlines from NewsAPI ===\n"
    news_summary += "\n\n".join([
        f"[{i+1}] {item.title}\nSource: {item.source}\nSummary: {item.summary or 'N/A'}"
        for i, item in enumerate(state.raw_news[:20])
    ])
    
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.3,
        max_output_tokens=500,
        google_api_key=settings.gemini_api_key,
    )
    
    system_prompt = await get_topic_selector_prompt()
    
    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": news_summary}
    ])
    
    try:
        result = json.loads(response.content)
        state.selected_topic = result.get("topic")
        state.selection_reasoning = result.get("reasoning")
    except:
        state.selected_topic = response.content.strip()
    
    logger.info(f"✓ Selected topic: {state.selected_topic}")
    return state

