# TechSnack AI Content Generator - Detailed Implementation Plan

## System Architecture

**Local Python application** with two workflow modes:

1. **Auto-discovery mode**: Fetch tech news → Select best topic → Deep research → Generate TechSnack article
2. **Manual topic mode**: User provides topic → Deep research → Generate TechSnack article

**Tech Stack:**

- Python 3.12+
- LangGraph 1.0+ for workflow orchestration
- Streamlit for UI
- Gemini 2.5 Flash Preview (gemini-2.5-flash-preview-09-2025)
- News APIs: NewsAPI + Google News RSS + Hacker News API
- Tavily API for deep research (free tier)
- Langfuse for AI observability (optional)
- Local file storage (markdown)

## Project Structure

Following financial-data-agent pattern:

```
techsnack-ai/
├── pyproject.toml              # Dependencies & config
├── .env.example                # Environment template
├── .env                        # API keys (gitignored)
├── README.md
├── app.py                      # Streamlit UI entry point
├── src/
│   └── techsnack/
│       ├── __init__.py
│       ├── config.py           # Settings with pydantic-settings
│       ├── main.py             # Optional FastAPI if needed later
│       ├── models.py           # Pydantic models
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── state.py        # LangGraph state schema
│       │   ├── graph.py        # Workflow definition
│       │   └── nodes/
│       │       ├── __init__.py
│       │       ├── news_fetcher_node.py
│       │       ├── topic_selector_node.py
│       │       ├── researcher_node.py
│       │       └── writer_node.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── news_fetcher.py     # News API integrations
│       │   └── web_search.py       # Tavily/search tools
│       ├── llms/
│       │   ├── __init__.py
│       │   └── manager.py          # LLM instance management
│       └── prompts/
│           ├── __init__.py
│           ├── prompts.py          # Prompt loader
│           ├── topic_selector.md   # Topic selection prompt
│           ├── writer.md           # Writer system prompt
│           └── examples/
│               ├── techsnack_01_cursor.md
│               ├── techsnack_02_rag.md
│               └── ...
├── outputs/                    # Generated articles
└── requirements.txt            # Frozen dependencies
```

## Detailed Implementation

### 1. Configuration (`src/techsnack/config.py`)

```python
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")
    newsapi_key: str = os.environ.get("NEWSAPI_KEY", "")
    tavily_api_key: str = os.environ.get("TAVILY_API_KEY", "")
    
    # Optional: Langfuse
    langfuse_host: str | None = os.environ.get("LANGFUSE_HOST")
    langfuse_public_key: str | None = os.environ.get("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str | None = os.environ.get("LANGFUSE_SECRET_KEY")
    
    # App settings
    output_dir: str = "outputs"
    max_news_items: int = 30
    research_depth: int = 5  # Max search results per topic
    
    # LLM settings
    gemini_model: str = "gemini-2.5-flash-preview-09-2025"
    gemini_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 2. State Schema (`src/techsnack/graph/state.py`)

```python
from typing import Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NewsItem(BaseModel):
    title: str
    url: str
    source: str
    published_at: str
    summary: str | None = None
    score: float = 0.0  # Relevance score

class ResearchData(BaseModel):
    topic: str
    sources: list[dict[str, Any]] = []  # Web search results
    key_facts: list[str] = []
    technical_details: str = ""
    context: str = ""

class TechSnackState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # Mode
    mode: str  # "auto" or "manual"
    
    # Input
    user_topic: str | None = None
    
    # Auto mode: news fetching
    raw_news: list[NewsItem] = []
    
    # Topic selection
    selected_topic: str | None = None
    selection_reasoning: str | None = None
    
    # Research
    research_data: ResearchData | None = None
    
    # Article generation
    article: str | None = None
    article_metadata: dict[str, Any] = {}
    
    # Timestamps
    started_at: datetime | None = None
    completed_at: datetime | None = None
```

### 3. Graph Workflow (`src/techsnack/graph/graph.py`)

```python
from langgraph.graph import StateGraph, END
import logging

from .nodes import (
    news_fetcher_node,
    topic_selector_node,
    researcher_node,
    writer_node,
)
from .state import TechSnackState

logger = logging.getLogger(__name__)

def route_after_input(state: TechSnackState) -> str:
    """Route based on mode."""
    if state.mode == "manual":
        return "researcher"
    return "news_fetcher"

def create_techsnack_graph():
    """Create TechSnack LangGraph workflow."""
    logger.info("Creating TechSnack graph")
    
    workflow = StateGraph(TechSnackState)
    
    # Add nodes
    workflow.add_node("news_fetcher", news_fetcher_node)
    workflow.add_node("topic_selector", topic_selector_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    
    # Define workflow
    workflow.set_conditional_entry_point(route_after_input)
    
    # Auto mode path
    workflow.add_edge("news_fetcher", "topic_selector")
    workflow.add_edge("topic_selector", "researcher")
    
    # Both modes converge at researcher
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    compiled = workflow.compile()
    logger.info("TechSnack graph compiled successfully")
    
    return compiled
```

### 4. Node: News Fetcher (`src/techsnack/graph/nodes/news_fetcher_node.py`)

```python
import logging
from datetime import datetime, timedelta
import asyncio

from ..state import TechSnackState, NewsItem
from ...tools.news_fetcher import (
    fetch_newsapi,
    fetch_hackernews,
    fetch_google_news_rss,
)

logger = logging.getLogger(__name__)

async def news_fetcher_node(state: TechSnackState) -> TechSnackState:
    """Fetch tech news from multiple sources in parallel."""
    logger.info("Fetching tech news...")
    
    # Fetch from all sources in parallel
    results = await asyncio.gather(
        fetch_newsapi(
            query="AI OR machine learning OR developer tools",
            from_date=(datetime.now() - timedelta(days=1)),
        ),
        fetch_hackernews(limit=20),
        fetch_google_news_rss(query="technology AI"),
        return_exceptions=True
    )
    
    all_news = []
    for result in results:
        if isinstance(result, list):
            all_news.extend(result)
        else:
            logger.warning(f"News fetch failed: {result}")
    
    # Convert to NewsItem objects
    state.raw_news = [
        NewsItem(**item) if isinstance(item, dict) else item
        for item in all_news
    ]
    
    logger.info(f"Fetched {len(state.raw_news)} news items")
    return state
```

### 5. Node: Topic Selector (`src/techsnack/graph/nodes/topic_selector_node.py`)

```python
import logging
import json
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts import get_topic_selector_prompt
from ...config import settings

logger = logging.getLogger(__name__)

async def topic_selector_node(state: TechSnackState) -> TechSnackState:
    """Use LLM to select best 1-2 topics from news."""
    logger.info("Selecting best topics...")
    
    # Prepare news summary for LLM
    news_summary = "\n\n".join([
        f"[{i+1}] {item.title}\nSource: {item.source}\nURL: {item.url}\nSummary: {item.summary or 'N/A'}"
        for i, item in enumerate(state.raw_news[:30])
    ])
    
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.3,  # Lower for selection
        max_output_tokens=500,
    )
    
    system_prompt = await get_topic_selector_prompt()
    
    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Today's tech news:\n\n{news_summary}"}
    ])
    
    # Parse response (expect JSON with topic and reasoning)
    try:
        result = json.loads(response.content)
        state.selected_topic = result.get("topic")
        state.selection_reasoning = result.get("reasoning")
    except:
        # Fallback: use raw content as topic
        state.selected_topic = response.content.strip()
    
    logger.info(f"Selected topic: {state.selected_topic}")
    return state
```

### 6. Node: Researcher (`src/techsnack/graph/nodes/researcher_node.py`)

```python
import logging
from ...tools.web_search import tavily_search
from ..state import TechSnackState, ResearchData
from ...config import settings

logger = logging.getLogger(__name__)

async def researcher_node(state: TechSnackState) -> TechSnackState:
    """Deep dive research on selected/manual topic."""
    topic = state.selected_topic or state.user_topic
    logger.info(f"Researching topic: {topic}")
    
    # Perform web search
    search_results = await tavily_search(
        query=topic,
        max_results=settings.research_depth,
        include_domains=["github.com", "techcrunch.com", "medium.com", "dev.to"]
    )
    
    # Structure research data
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
    logger.info(f"Research completed with {len(search_results)} sources")
    return state
```

### 7. Node: Writer (`src/techsnack/graph/nodes/writer_node.py`)

```python
import logging
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts import get_writer_prompt, load_techsnack_examples
from ...config import settings

logger = logging.getLogger(__name__)

async def writer_node(state: TechSnackState) -> TechSnackState:
    """Generate TechSnack article in Vietnamese style."""
    logger.info("Writing TechSnack article...")
    
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.7,
        max_output_tokens=2048,
    )
    
    # Build context
    topic = state.selected_topic or state.user_topic
    research_context = state.research_data.context if state.research_data else ""
    
    # Load few-shot examples
    examples = await load_techsnack_examples()
    
    system_prompt = await get_writer_prompt()
    user_prompt = f"""
Topic: {topic}

Research Context:
{research_context}

Please write a TechSnack article following the style in the examples.
Target length: 1-2 minute read (~300-400 words in Vietnamese).
"""
    
    response = await llm.ainvoke([
        {"role": "system", "content": system_prompt + "\n\n" + examples},
        {"role": "user", "content": user_prompt}
    ])
    
    state.article = response.content
    state.article_metadata = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "word_count": len(response.content.split()),
    }
    state.completed_at = datetime.now()
    
    logger.info("Article generation completed")
    return state
```

### 8. Prompts (`src/techsnack/prompts/`)

**prompts.py** - Loader utility (following financial-agent pattern):

```python
from pathlib import Path
from datetime import datetime

PROMPTS_DIR = Path(__file__).parent

def load_prompt(filename: str) -> str:
    """Load prompt from markdown file."""
    filepath = PROMPTS_DIR / filename
    return filepath.read_text() if filepath.exists() else ""

# Load prompts
TOPIC_SELECTOR_PROMPT = load_prompt("topic_selector.md")
WRITER_PROMPT = load_prompt("writer.md")

async def get_topic_selector_prompt() -> str:
    """Get topic selector prompt with date injection."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    return TOPIC_SELECTOR_PROMPT.replace("{{date}}", today)

async def get_writer_prompt() -> str:
    """Get writer prompt."""
    return WRITER_PROMPT

async def load_techsnack_examples() -> str:
    """Load example TechSnack articles for few-shot learning."""
    examples_dir = PROMPTS_DIR / "examples"
    examples = []
    
    for file in sorted(examples_dir.glob("*.md")):
        content = file.read_text()
        examples.append(f"=== Example: {file.stem} ===\n{content}\n")
    
    return "\n\n".join(examples)
```

**topic_selector.md**:

```markdown
You are a tech content curator for Viet Tech Community in Finland.

Today's date: {{date}}

Your task is to analyze today's tech news and select the BEST 1 topic for a TechSnack article.

## Selection Criteria

1. **AI & Developer Tools Focus**: Prefer AI advancements, new developer tools, major tech announcements
2. **Educational Value**: Should teach developers something practical or conceptual
3. **Community Relevance**: Interesting for Vietnamese developers in Finland
4. **Freshness**: Breaking news or trending topics
5. **TechSnack Style Fit**: Can be explained casually in 1-2 min read

## Output Format

Return JSON with:
{
  "topic": "Clear, specific topic title",
  "reasoning": "Why this topic is best for today's TechSnack"
}

Focus on topics that can be explained with analogies, practical examples, and developer-friendly language.
```

**writer.md**:

```markdown
You are a Vietnamese tech content writer for TechSnack series - a casual, engaging tech education series for Viet Tech Community in Finland.

## Writing Guidelines

1. **Tone**: Casual, friendly Vietnamese (like talking to fellow devs over coffee)
2. **Structure**:
   - Hook with context from previous TechSnack or current trend
   - Explain concept with dev-friendly analogies
   - Show practical examples or how it works
   - Why it matters to developers
   - Call-to-action: Ask community to share experiences

3. **Language**:
   - Mix Vietnamese and English tech terms naturally (e.g., "RAG", "AI", "production")
   - Use "ae" (anh em), "mình", "bạn" for casual tone
   - Explain with "kiểu" comparisons

4. **Length**: 300-400 words Vietnamese (~1-2 min read)

5. **Format**:
   - Start with title: [#TechSnack XX] | Topic
   - Reference previous TechSnack if relevant
   - Include practical use cases
   - End with community engagement questions

## Style Examples

Below are example TechSnack articles showing the desired tone and structure.
```

### 9. Streamlit UI (`app.py`)

```python
import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path

from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState
from src.techsnack.config import settings

st.set_page_config(page_title="TechSnack AI Generator", page_icon="📰")

st.title("🇻🇳 TechSnack AI Generator")
st.caption("Automated tech content for Viet Tech Community")

# Initialize graph
@st.cache_resource
def get_graph():
    return create_techsnack_graph()

graph = get_graph()

# Tabs
tab1, tab2 = st.tabs(["🤖 Auto Generate", "✏️ Manual Topic"])

# Tab 1: Auto Generate
with tab1:
    st.subheader("Auto-Generate Today's TechSnack")
    st.write("System will fetch latest tech news, select best topic, research, and write article.")
    
    if st.button("Generate Today's TechSnack", type="primary"):
        with st.spinner("Fetching news..."):
            placeholder = st.empty()
            
            # Create state
            initial_state = TechSnackState(
                mode="auto",
                started_at=datetime.now()
            )
            
            # Run graph
            result = asyncio.run(graph.ainvoke(initial_state))
            
            # Display results
            st.success("✅ Article Generated!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Topic", result.selected_topic)
            with col2:
                st.metric("Word Count", result.article_metadata.get("word_count", 0))
            
            st.markdown("### 📝 Article Preview")
            st.markdown(result.article)
            
            # Save & download
            filename = f"techsnack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_path = Path(settings.output_dir) / filename
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(result.article)
            
            st.download_button(
                "⬇️ Download Article",
                data=result.article,
                file_name=filename,
                mime="text/markdown"
            )

# Tab 2: Manual Topic
with tab2:
    st.subheader("Generate from Custom Topic")
    
    topic_input = st.text_area(
        "Enter your topic:",
        placeholder="e.g., Vector databases for AI applications",
        height=100
    )
    
    if st.button("Research & Generate", type="primary", disabled=not topic_input):
        with st.spinner(f"Researching '{topic_input}'..."):
            initial_state = TechSnackState(
                mode="manual",
                user_topic=topic_input,
                started_at=datetime.now()
            )
            
            result = asyncio.run(graph.ainvoke(initial_state))
            
            st.success("✅ Article Generated!")
            st.markdown("### 📝 Article Preview")
            st.markdown(result.article)
            
            filename = f"techsnack_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            st.download_button(
                "⬇️ Download Article",
                data=result.article,
                file_name=filename,
                mime="text/markdown"
            )
```

### 10. Dependencies (`pyproject.toml`)

```toml
[project]
name = "techsnack-ai"
version = "0.1.0"
description = "LangGraph-based TechSnack content generator"
requires-python = ">=3.12"
dependencies = [
    "langgraph>=1.0.0",
    "langchain-core>=0.3.0",
    "langchain-google-genai>=2.0.0",
    "streamlit>=1.40.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "aiohttp>=3.11.0",
    "httpx>=0.27.0",
    "tavily-python>=0.5.0",
    "newsapi-python>=0.2.7",
    "feedparser>=6.0.0",  # For RSS
    "langfuse>=2.0.0",  # Optional
]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I"]
```

## Implementation Todos Summary

1. **Setup project structure** - Create directories, pyproject.toml, virtual env
2. **Implement configuration** - Settings, .env template
3. **Create state schema** - Define TechSnackState with all fields
4. **Build news fetcher tools** - NewsAPI, HackerNews, RSS integrations
5. **Build web search tool** - Tavily integration for research
6. **Implement news fetcher node** - Parallel fetching logic
7. **Implement topic selector node** - LLM-based selection
8. **Implement researcher node** - Deep research orchestration
9. **Implement writer node** - Article generation with few-shot
10. **Create LangGraph workflow** - Assemble all nodes with routing
11. **Write prompts** - topic_selector.md, writer.md with examples
12. **Build Streamlit UI** - Two-tab interface with progress tracking
13. **Add output handling** - File saving, download buttons
14. **Test end-to-end** - Both auto and manual modes

## Key Features

- **Clean Architecture**: Following proven financial-agent pattern
- **Type Safety**: Full Pydantic models for state and data
- **Async First**: All I/O operations are async
- **Prompt Management**: Markdown files with template variables
- **Few-Shot Learning**: Include 2-3 example TechSnack articles
- **Observability**: Optional Langfuse integration
- **Cost Effective**: Gemini 2.5 Flash (~$0.01 per article)