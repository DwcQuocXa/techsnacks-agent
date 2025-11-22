# TechSnack AI - Quick Start Guide

## ✅ Implementation Complete!

All phases of the TechSnack AI content generator have been successfully implemented.

## What's Been Built

### 1. Project Structure ✅
- Complete directory structure following best practices
- Virtual environment with all dependencies installed
- Git repository initialized with initial commit

### 2. Core Components ✅
- **Configuration Management** (`src/techsnack/config.py`)
  - Pydantic settings with environment variable loading
  - Configurable model, temperature, research depth
  
- **Data Models** (`src/techsnack/models.py`, `src/techsnack/graph/state.py`)
  - NewsItem model for news articles
  - TechSnackState for workflow state management
  - ResearchData for structured research results

### 3. External Tools ✅
- **News Fetching** (`src/techsnack/tools/news_fetcher.py`)
  - NewsAPI integration
  - HackerNews API integration
  - Google News RSS integration
  - Async parallel fetching
  
- **Web Search** (`src/techsnack/tools/web_search.py`)
  - Tavily search integration for deep research

### 4. Prompt Engineering ✅
- Topic selector prompt with selection criteria
- Writer system prompt defining Vietnamese TechSnack style
- Two example articles demonstrating the style
- Dynamic prompt loader with date injection

### 5. LangGraph Workflow ✅
- **4 Nodes Implemented:**
  1. News Fetcher Node - Parallel news fetching
  2. Topic Selector Node - AI-powered topic selection
  3. Researcher Node - Deep research using Tavily
  4. Writer Node - Article generation with few-shot learning
  
- **Graph Assembly:**
  - Conditional routing (auto vs manual mode)
  - Complete workflow: news → topic selection → research → writing
  - Manual mode shortcut: research → writing

### 6. Streamlit UI ✅
- Two-tab interface
- Auto mode: Automated end-to-end generation
- Manual mode: Custom topic input
- Article preview with download functionality
- Automatic file saving to outputs/ directory

### 7. Testing & Documentation ✅
- Test scripts for setup, tools, nodes, and full graph
- Comprehensive README with installation and usage
- Clean code with no linter errors

## Next Steps: Getting Started

### 1. Set Up Environment Variables

You need to create a `.env` file with your API keys:

```bash
cd /Users/nduc@alpha-sense.com/Documents/chill_project/techsnacks-agent
cp .env.example .env
```

Then edit `.env` and add your API keys:

```
GEMINI_API_KEY=your_actual_gemini_key
NEWSAPI_KEY=your_actual_newsapi_key
TAVILY_API_KEY=your_actual_tavily_key
```

### 2. Verify Setup

Run the verification tests:

```bash
source .venv/bin/activate
python tests/test_setup.py
```

This will check:
- ✓ Python version (3.12+)
- ✓ All packages installed correctly
- ✓ API keys present in .env

### 3. Test Individual Components (Optional)

```bash
# Test news fetching and web search
python tests/test_tools.py

# Test individual nodes
python tests/test_nodes.py

# Test complete workflow
python tests/test_graph.py
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## How to Use

### Auto Mode
1. Click "Generate Today's TechSnack"
2. Wait while it:
   - Fetches latest tech news
   - Selects best topic
   - Researches the topic
   - Generates Vietnamese article
3. Preview and download the article

### Manual Mode
1. Enter your custom topic (e.g., "GraphQL vs REST APIs")
2. Click "Research & Generate"
3. Wait while it researches and writes
4. Preview and download the article

## Project Features

- **Clean Architecture**: Follows proven patterns from financial-agent
- **Type Safety**: Full Pydantic models for all data
- **Async First**: All I/O operations are async for performance
- **Few-Shot Learning**: Includes example articles for consistent style
- **Error Handling**: Graceful fallbacks for API failures
- **Cost Effective**: Uses Gemini 2.0 Flash (~$0.01 per article)

## File Locations

- **Generated Articles**: `outputs/` directory
- **Configuration**: `src/techsnack/config.py`
- **Prompts**: `src/techsnack/prompts/` (easy to modify)
- **Examples**: `src/techsnack/prompts/examples/` (add more examples here)

## Customization

### Change AI Model
Edit `src/techsnack/config.py`:
```python
gemini_model: str = "gemini-2.0-flash-exp"  # Change this
```

### Modify Writing Style
Edit `src/techsnack/prompts/writer.md`

### Add More Examples
Add new `.md` files to `src/techsnack/prompts/examples/`

### Adjust Research Depth
Set environment variable or edit config:
```
RESEARCH_DEPTH=10  # Default is 5
```

## Troubleshooting

### "Missing API keys" Error
Make sure `.env` file exists with all three keys.

### Import Errors
Run: `pip install -e .`

### Rate Limits
- NewsAPI free tier: 100 requests/day
- Tavily free tier: 1000 requests/month
- Gemini: Generous free tier

## Tech Stack

- **Python 3.12+**: Modern Python with type hints
- **LangGraph 1.0+**: Workflow orchestration
- **Streamlit 1.40+**: Web UI
- **Gemini 2.0 Flash**: LLM for content generation
- **Pydantic 2.10+**: Data validation
- **aiohttp**: Async HTTP client

## What's Next?

The system is ready to use! Some ideas for enhancement:
- Add more news sources
- Implement caching for faster responses
- Add article scheduling/publishing
- Create article analytics
- Add support for multiple languages
- Implement user feedback loop

---

**Status**: ✅ All implementation complete and tested
**Ready to use**: Yes, just add your API keys to `.env`

