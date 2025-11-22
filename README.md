# TechSnack AI Content Generator

Automated Vietnamese tech content generator using LangGraph, powered by Gemini 2.0.

## Overview

TechSnack AI automatically generates casual, engaging tech articles in Vietnamese for the Viet Tech Community in Finland. It features two modes:

- **Auto mode**: Fetches latest tech news → selects best topic → researches → writes article
- **Manual mode**: Takes user topic → researches → writes article

## Prerequisites

- Python 3.12+
- API Keys:
  - Google Gemini API key
  - NewsAPI key
  - Tavily API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd techsnacks-agent
```

2. Create virtual environment:
```bash
python3.12 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR: .venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -e .
```

4. Setup environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
NEWSAPI_KEY=your_newsapi_key
TAVILY_API_KEY=your_tavily_api_key
```

## Getting API Keys

- **Gemini API**: https://ai.google.dev/ (Free tier available)
- **NewsAPI**: https://newsapi.org/ (Free tier: 100 requests/day)
- **Tavily API**: https://tavily.com/ (Free tier: 1000 requests/month)

## Usage

### Run Streamlit App

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### Test Setup

Verify everything is working:

```bash
python tests/test_setup.py
python tests/test_tools.py
python tests/test_graph.py
```

## Project Structure

```
techsnacks-agent/
├── app.py                  # Streamlit UI
├── src/techsnack/
│   ├── config.py          # Settings management
│   ├── models.py          # Data models
│   ├── graph/
│   │   ├── state.py       # LangGraph state
│   │   ├── graph.py       # Workflow definition
│   │   └── nodes/         # Individual workflow nodes
│   ├── tools/
│   │   ├── news_fetcher.py    # News APIs
│   │   └── web_search.py      # Tavily search
│   └── prompts/
│       ├── prompts.py         # Prompt loader
│       ├── topic_selector.md  # Topic selection prompt
│       ├── writer.md          # Writer prompt
│       └── examples/          # Example articles
├── tests/                 # Test scripts
└── outputs/              # Generated articles
```

## How It Works

### Auto Mode
1. Fetches tech news from NewsAPI, HackerNews, Google News
2. LLM selects best topic based on criteria
3. Researches topic using Tavily search
4. Generates Vietnamese article in TechSnack style

### Manual Mode
1. User provides topic
2. Researches topic using Tavily search
3. Generates Vietnamese article in TechSnack style

## Configuration

Edit `src/techsnack/config.py` or set environment variables:

- `GEMINI_MODEL`: Model name (default: "gemini-2.0-flash-exp")
- `GEMINI_TEMPERATURE`: Temperature 0-1 (default: 0.7)
- `MAX_NEWS_ITEMS`: Max news to fetch (default: 30)
- `RESEARCH_DEPTH`: Max search results (default: 5)
- `OUTPUT_DIR`: Output directory (default: "outputs")

## Troubleshooting

### Missing API Keys Error
Make sure `.env` file exists with all three API keys set.

### Import Errors
Reinstall dependencies: `pip install -e .`

### NewsAPI Rate Limit
Free tier is limited to 100 requests/day. Consider upgrading or reducing test frequency.

### Gemini API Errors
Check your API key is valid and has quota remaining.

## Development

### Adding New News Sources
Edit `src/techsnack/tools/news_fetcher.py` and add new async function.

### Modifying Prompts
Edit markdown files in `src/techsnack/prompts/`

### Adding Examples
Add new `.md` files to `src/techsnack/prompts/examples/`

## License

MIT

