# TechSnack AI Content Generator

Automated Vietnamese tech content generator using LangGraph, powered by Gemini 2.0.

## Overview

TechSnack AI automatically generates casual, engaging tech articles in Vietnamese for the Viet Tech Community in Finland. It features two modes:

- **Auto mode**: Fetches latest tech news → selects best topic → researches → writes article
- **Manual mode**: Takes user topic → researches → writes article

## Quick Start

### One-Command Start

```bash
./start.sh
```

The start script will:
1. ✅ Check Python 3.12+ is installed
2. ✅ Create/activate virtual environment
3. ✅ Install all dependencies
4. ✅ Check for .env file and API keys
5. ✅ Start the Streamlit app

Then open http://localhost:8501 in your browser!

### Manual Setup

If you prefer to set things up manually:

1. **Create virtual environment:**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # OR: .venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Setup environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys.

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Prerequisites

- Python 3.12+
- API Keys:
  - Google Gemini API key
  - NewsAPI key
  - Tavily API key
  - Perplexity API key

## Getting API Keys

- **Gemini API**: https://ai.google.dev/ (Free tier available)
- **NewsAPI**: https://newsapi.org/ (Free tier: 100 requests/day)
- **Tavily API**: https://tavily.com/ (Free tier: 1000 requests/month)
- **Perplexity API**: https://www.perplexity.ai/settings/api (Free tier: 5 requests/month, $0.2/1K tokens after)

## Project Structure

```
techsnacks-agent/
├── start.sh               # 🆕 One-command start script
├── app.py                 # Streamlit UI entry point
├── src/techsnack/
│   ├── config.py         # Settings management
│   ├── models.py         # Data models
│   ├── graph/
│   │   ├── state.py      # LangGraph state
│   │   ├── graph.py      # Workflow definition
│   │   └── nodes/        # Individual workflow nodes
│   ├── tools/
│   │   ├── news_fetcher.py    # News APIs
│   │   ├── web_search.py      # Tavily search
│   │   ├── perplexity_search.py  # Perplexity integration
│   │   └── query_builder.py   # Smart queries
│   └── prompts/
│       ├── prompts.py         # Prompt loader
│       ├── topic_selector.md  # Topic selection prompt
│       ├── writer.md          # Writer prompt
│       └── examples/          # Example articles
├── tests/                # Test scripts
└── outputs/             # Generated articles
```

## How It Works

### Auto Mode
1. Fetches tech news from NewsAPI, HackerNews, Google News
2. **Uses Perplexity to discover today's best tech news with context**
3. LLM selects best topic based on criteria
4. **Researches topic using both Perplexity (deep analysis) and Tavily (broad coverage)**
5. Generates Vietnamese article in TechSnack style

### Manual Mode
1. User provides topic
2. **Researches topic using both Perplexity and Tavily**
3. Generates Vietnamese article in TechSnack style

## Configuration

Edit `src/techsnack/config.py` or set environment variables:

```
GEMINI_API_KEY=your_gemini_api_key
NEWSAPI_KEY=your_newsapi_key
TAVILY_API_KEY=your_tavily_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

Optional settings:
- `GEMINI_MODEL`: Model name (default: "gemini-2.0-flash-exp")
- `GEMINI_TEMPERATURE`: Temperature 0-1 (default: 0.7)
- `MAX_NEWS_ITEMS`: Max news to fetch (default: 30)
- `RESEARCH_DEPTH`: Max search results (default: 5)
- `OUTPUT_DIR`: Output directory (default: "outputs")

## Testing

Run verification tests:

```bash
# Test setup
python tests/test_setup.py

# Test external APIs
python tests/test_tools.py

# Test Perplexity integration
python tests/test_perplexity.py

# Test complete workflow
python tests/test_graph.py
```

## Troubleshooting

### Missing API Keys Error
Make sure `.env` file exists with all four API keys set.

### Import Errors
Reinstall dependencies: `pip install -e .`

### NewsAPI Rate Limit
Free tier is limited to 100 requests/day. Consider upgrading or reducing test frequency.

### Perplexity API Errors
Check your API key is valid and has quota remaining. Free tier: 5 requests/month.

### Permission Denied on start.sh
Make it executable: `chmod +x start.sh`

## Development

### Adding New News Sources
Edit `src/techsnack/tools/news_fetcher.py` and add new async function.

### Modifying Prompts
Edit markdown files in `src/techsnack/prompts/`

### Adding Examples
Add new `.md` files to `src/techsnack/prompts/examples/`

## Documentation

- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system diagrams
- **Quick Start Guide**: See [QUICKSTART.md](QUICKSTART.md) for detailed setup
- **Perplexity Integration**: See [PERPLEXITY_INTEGRATION.md](PERPLEXITY_INTEGRATION.md)

## Cost Estimate

**Per Auto-Generated Article:**
- News Discovery (Perplexity): ~$0.60
- Topic Research (Perplexity): ~$0.40
- Tavily: Free (1000/month)
- Gemini: Free (generous tier)

**Total: ~$1.00 per auto-generated article**

**Manual Mode**: ~$0.40 per article (no news discovery)

## License

MIT
