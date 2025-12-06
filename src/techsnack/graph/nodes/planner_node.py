import json
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore[import-untyped]

from ..state import TechSnackState
from ...config import settings
from ...prompts.prompts import get_planner_prompts
from ...logging_config import get_logger

logger = get_logger(__name__)

async def planner_node(state: TechSnackState) -> TechSnackState:
    topic = state.selected_topic or state.user_topic
    if not topic:
        logger.warning("⚠️ Planner skipped: no topic available")
        state.plan_topic = None
        state.plan_search_queries = []
        return state
    
    if state.writer_model.startswith("gemini"):
        llm = ChatGoogleGenerativeAI(
            model=state.writer_model,
            temperature=0.4,
            max_output_tokens=600,
            google_api_key=settings.gemini_api_key,
        )
        logger.info(f"🧠 Planning research with {state.writer_model}")
    else:
        llm = ChatOpenAI(
            model=state.writer_model,
            api_key=settings.openai_api_key,
            temperature=0.4,
        )
        logger.info(f"🧠 Planning research with {state.writer_model}")
    
    system_prompt, user_prompt = await get_planner_prompts(topic)
    
    logger.info(f"  → Topic: {topic}")
    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    
    content = response.content
    if isinstance(content, list):
        content = " ".join(str(part) for part in content)
    
    plan_topic, search_queries = _parse_plan_response(content, fallback_topic=topic)
    state.plan_topic = plan_topic
    state.plan_search_queries = search_queries
    
    logger.info(f"✓ Planner produced {len(search_queries)} search queries")
    return state


def _parse_plan_response(content: str, fallback_topic: str) -> tuple[str, list[str]]:
    if not content:
        return fallback_topic, [fallback_topic]

    # Strip markdown code fences if present
    content_cleaned = content.strip()
    if content_cleaned.startswith("```"):
        # Remove opening fence (```json or ```)
        lines = content_cleaned.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        # Remove closing fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content_cleaned = "\n".join(lines).strip()

    # Try to extract JSON from the response
    try:
        data = json.loads(content_cleaned)
        topic = data.get("topic") or fallback_topic
        queries = data.get("search_queries") or []
    except json.JSONDecodeError:
        logger.warning(f"⚠️ Failed to parse planner JSON. Raw response: {content[:200]}...")
        # Fallback: try to find JSON-like content
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end > start:
            try:
                data = json.loads(content[start:end])
                topic = data.get("topic") or fallback_topic
                queries = data.get("search_queries") or []
            except json.JSONDecodeError:
                logger.warning("⚠️ Fallback JSON extraction also failed, using topic as sole query")
                topic = fallback_topic
                queries = [fallback_topic]
        else:
            topic = fallback_topic
            queries = [fallback_topic]

    # Clean and validate queries
    cleaned_queries = []
    seen = set()
    for q in queries:
        if not isinstance(q, str):
            continue
        q = q.strip()
        # Skip invalid queries (too short, just punctuation, etc.)
        if not q or len(q) < 5:
            continue
        # Skip queries that are just punctuation or special characters
        if all(c in "{}[]().,;:!?-—–_\"'`~@#$%^&*+=<>|\\/" for c in q):
            continue
        q = q[:120]
        if q.lower() in seen:
            continue
        seen.add(q.lower())
        cleaned_queries.append(q)

    if not cleaned_queries:
        logger.warning(f"⚠️ No valid queries extracted, using fallback topic: {fallback_topic}")
        cleaned_queries = [fallback_topic]

    logger.info(f"  ✓ Parsed plan: topic='{topic}', queries={len(cleaned_queries)}")
    return topic, cleaned_queries

