import json
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts.prompts import get_topic_selector_prompt
from ...config import settings

async def topic_selector_node(state: TechSnackState) -> TechSnackState:
    news_summary = "\n\n".join([
        f"[{i+1}] {item.title}\nSource: {item.source}\nURL: {item.url}\nSummary: {item.summary or 'N/A'}"
        for i, item in enumerate(state.raw_news[:30])
    ])
    
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.3,
        max_output_tokens=500,
    )
    
    system_prompt = await get_topic_selector_prompt()
    
    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Today's tech news:\n\n{news_summary}"}
    ])
    
    try:
        result = json.loads(response.content)
        state.selected_topic = result.get("topic")
        state.selection_reasoning = result.get("reasoning")
    except:
        state.selected_topic = response.content.strip()
    
    return state

