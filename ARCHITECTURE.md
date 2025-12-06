# TechSnack AI – Planner-Centric Architecture

This document captures the latest planner-first design for TechSnack AI.

---

## Pipeline Overview

### Auto Mode
1. **News Fetcher** – pulls breaking AI/dev-tools headlines from NewsAPI, summarizes them, then asks Perplexity to rank 3‑5 candidate topics for engineers. Output: `raw_news`, `today_topics`.
2. **Topic Selector** – GPT (via `ChatOpenAI`) inspects `today_topics` and chooses the single best topic + reasoning.
3. **Planner** – generates a minimal JSON plan: `{ "topic": "...", "search_queries": ["q1", "q2", ...] }`.
4. **Researcher** – iterates the planner's short queries through the unified search layer (Perplexity + Tavily) and aggregates sources/contexts.
5. **Writer** – composes the final TechSnack article using the research context and style examples.

### Manual Mode
1. User submits a topic from the Streamlit UI (with optional instructions).
2. Planner creates research queries for that topic.
3. Researcher aggregates facts based on the queries.
4. Writer produces the article.

Both modes share the same planner → researcher → writer chain. The Planner and Writer use the same configurable model (`writer_model`).

---

## Node Responsibilities

| Node | Responsibility | Key APIs |
|------|----------------|----------|
| `news_fetcher_node` | NewsAPI fetch + Perplexity ranking → `today_topics` | NewsAPI, Perplexity |
| `topic_selector_node` | GPT chooses the final topic for engineers | OpenAI (ChatOpenAI) |
| `planner_node` | Produces `{topic, search_queries[]}` | Configurable (Gemini or OpenAI) |
| `researcher_node` | Runs planner queries through `unified_search` and aggregates research data | Tavily + Perplexity |
| `writer_node` | Writes the final Vietnamese TechSnack article | Configurable (Gemini or OpenAI) |

State fields tied to this flow:
- `today_topics`: Perplexity-ranked auto-mode candidates.
- `selected_topic`, `selection_reasoning`: topic selector output.
- `plan_topic`, `plan_search_queries`: planner output (shared auto/manual).
- `research_data`, `article`, `article_metadata`: downstream results.
- `writer_model`: configurable model for planner and writer nodes.
- `user_query`: optional user instructions for the writer.

---

## Data Flow Summary

```
Auto mode:
START
  → news_fetcher (NewsAPI + Perplexity ranking)
  → topic_selector (GPT)
  → planner (configurable model)
  → researcher (Perplexity + Tavily)
  → writer (configurable model)
  → END

Manual mode:
START
  → planner (configurable model based on user topic)
  → researcher
  → writer
  → END
```

---

## LLM Usage

- **Topic Selector**: Always uses OpenAI GPT for concise JSON output.
- **Planner + Writer**: Use the `writer_model` setting, which can be:
  - `gpt-5` (default)
  - `gemini-2.5-flash-preview-09-2025`
  - `gemini-3-pro-preview`
- **Perplexity**: Auto-mode news enrichment/ranking and deep research responses.

---

## Unified Search Layer

`unified_search(query)` orchestrates:
1. Perplexity – deep, citation-rich answer (if needed).
2. Tavily – fast web snippets with developer-friendly metadata.

Combined outputs are tagged with:
- `source_engine`: `"Perplexity"` or `"Tavily"`
- `query_used`: which planner query produced the source

Researcher node stores the merged results inside `ResearchData`.

---

## Testing Matrix (Mock Friendly)

| Test | Purpose | Notes |
|------|---------|-------|
| `tests/test_nodes.py` | Unit tests for news fetcher, planner, researcher | Uses mocked I/O |
| `tests/test_graph.py` | Validates auto/manual routing in LangGraph | Nodes mocked for determinism |
| `tests/test_tools.py` | Integration tests for external tools (optional) | Hits real APIs |
| `tests/test_perplexity.py` | Verifies Perplexity integration | Optional due to cost |

---

## Configuration Quick Reference

```env
GEMINI_API_KEY=...
NEWSAPI_KEY=...
TAVILY_API_KEY=...
PERPLEXITY_API_KEY=...
OPENAI_API_KEY=...
```

Optional settings in `config.py`:
- `openai_model`: defaults to `"gpt-5"`
- `gemini_model`: planner/writer model (`"gemini-2.0-flash-exp"`)
- `perplexity_model`: `"sonar"`
- `research_depth`, `max_news_items`, `output_dir`

---

## Cost Notes (Approx.)

- Auto mode: ~$1/article (NewsAPI + Perplexity ranking + LLM writing + per-query research)
- Manual mode: ~$0.40/article (skips news ranking)

Tavily is free (1k requests/month). Gemini planner calls are inexpensive; OpenAI GPT is the primary cost driver when selected.
