import json
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts.prompts import get_topic_selector_prompt
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)

async def topic_selector_node(state: TechSnackState) -> TechSnackState:
    candidate_topics = state.today_topics or _fallback_topics_from_news(state.raw_news)

    if not candidate_topics:
        logger.warning("⚠️ No candidate topics available; skipping topic selection")
        state.selected_topic = None
        state.selection_reasoning = None
        return state

    llm = ChatGoogleGenerativeAI(
        model=state.writer_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.6,
    )
    logger.info(f"🎯 Selecting best topic with {state.writer_model}")

    system_prompt = "You are the expert tech content curator for TechSnack, a daily tech digest for Vietnamese software engineers, tech leaders, and AI startup founders in Finland."
    user_prompt = await get_topic_selector_prompt()
    user_payload = json.dumps({"today_topics": candidate_topics}, ensure_ascii=False, indent=2)

    prompt_length = len(system_prompt) + len(user_prompt) + len(user_payload)
    logger.info(f"  📤 Payload preview: {user_payload[:200]}...")

    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + "\n\n" + user_payload}
    ])

    content = response.content
    if isinstance(content, list):
        parts = [p["text"] if isinstance(p, dict) and "text" in p else str(p) for p in content]
        content = "".join(parts)
    
    selected_topic, reasoning = _parse_topic_response(content)
    state.selected_topic = selected_topic
    state.selection_reasoning = reasoning

    logger.info(f"✓ Selected topic: {state.selected_topic}")
    return state


def _fallback_topics_from_news(raw_news: list, limit: int = 5) -> list[dict]:
    fallback = []
    for item in raw_news[:limit]:
        title = getattr(item, "title", "Untitled")
        summary = getattr(item, "summary", "") or f"Trending update from {getattr(item, 'source', 'Unknown')}."
        url = getattr(item, "url", "")
        fallback.append({
            "topic": title,
            "reason": summary,
            "fame_score": 5,
            "sources": [url] if url else [],
        })
    return fallback


def _parse_topic_response(content: str) -> tuple[str | None, str | None]:
    if not content:
        return None, None
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return content.strip(), None
    
    topic = data.get("topic")
    reason = data.get("reason") or data.get("reasoning")
    return topic, reason
