import json
from typing import Any
from datetime import datetime, timedelta

from ..state import TechSnackState
from ...tools.news_fetcher import fetch_newsapi
from ...tools.perplexity_search import perplexity_search
from ...prompts.prompts import get_news_discovery_prompt
from ...logging_config import get_logger

logger = get_logger(__name__)

async def news_fetcher_node(state: TechSnackState) -> TechSnackState:
    logger.info("📰 Fetching tech news from NewsAPI...")

    # Expanded query to cover broader tech news: AI, tools, big tech, startups, layoffs, leadership
    news_items = await fetch_newsapi(
        query=(
            "AI OR machine learning OR developer tools OR startup OR "
            "tech layoffs OR cloud computing OR open source OR "
            "cybersecurity OR tech CEO OR FAANG OR big tech"
        ),
        from_date=(datetime.now() - timedelta(days=1)),
    )
    
    state.raw_news = news_items
    logger.info(f"✓ Fetched {len(news_items)} news items from NewsAPI")
    
    if not news_items:
        state.today_topics = []
        return state
    
    headlines = _format_headlines(news_items)
    prompt = await get_news_discovery_prompt(headlines)
    
    logger.info("🔢 Asking Perplexity for top engineer-friendly topics...")
    result = await perplexity_search(prompt)
    today_topics = _parse_today_topics(result.get("answer", ""))
    
    if not today_topics:
        today_topics = _fallback_topics(news_items)
        logger.warning("  ⚠️ Perplexity result could not be parsed; using fallback topics")
    
    state.today_topics = today_topics
    logger.info(f"✓ Prepared {len(today_topics)} candidate topics")
    return state


def _format_headlines(news_items: list, limit: int = 10) -> str:
    lines = []
    for idx, item in enumerate(news_items[:limit], start=1):
        summary = (getattr(item, "summary", "") or "").replace("\n", " ").strip()
        source = getattr(item, "source", "Unknown")
        title = getattr(item, "title", "Untitled")
        lines.append(f"{idx}. {title} (Source: {source}) - {summary}")
    return "\n".join(lines)


def _parse_today_topics(answer: str) -> list[dict[str, Any]]:
    if not answer:
        return []
    
    json_candidates = _extract_json_candidates(answer)
    for candidate in json_candidates:
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        
        topics = data.get("today_topics")
        if isinstance(topics, list):
            cleaned = []
            for entry in topics:
                topic = entry.get("topic")
                reason = entry.get("reason", "")
                fame_score = entry.get("fame_score", 5)
                sources = entry.get("sources", [])
                category = entry.get("category", "General Tech")  # Default category if missing
                if topic:
                    cleaned.append({
                        "topic": topic,
                        "reason": reason,
                        "fame_score": fame_score,
                        "category": category,
                        "sources": sources if isinstance(sources, list) else [sources],
                    })
            if cleaned:
                return cleaned
    return []


def _extract_json_candidates(text: str) -> list[str]:
    text = text.strip()
    candidates = []
    
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.lower().startswith("json"):
                candidates.append(part[4:].strip())
            elif part.startswith("{"):
                candidates.append(part)
    
    if text.startswith("{") and text.endswith("}"):
        candidates.append(text)
    
    # Fallback: find first JSON-looking segment
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start:end+1])
    
    return candidates


def _fallback_topics(news_items: list, limit: int = 3) -> list[dict[str, Any]]:
    fallback = []
    for item in news_items[:limit]:
        title = getattr(item, "title", "Untitled")
        summary = getattr(item, "summary", "") or f"Trending update from {getattr(item, 'source', 'Unknown')}."
        url = getattr(item, "url", "")
        fallback.append({
            "topic": title,
            "reason": summary,
            "fame_score": 5,
            "category": "General Tech",
            "sources": [url] if url else [],
        })
    return fallback

