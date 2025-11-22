"""Verify all packages are installed and environment is configured."""
import sys

def test_python_version():
    assert sys.version_info >= (3, 12), f"Python 3.12+ required, got {sys.version}"
    print(f"✓ Python {sys.version}")

def test_imports():
    try:
        import streamlit
        print(f"✓ Streamlit {streamlit.__version__}")
    except ImportError as e:
        print(f"✗ Streamlit failed: {e}")
        raise

    try:
        import langgraph
        print(f"✓ LangGraph installed")
    except ImportError as e:
        print(f"✗ LangGraph failed: {e}")
        raise

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print(f"✓ Langchain Google GenAI installed")
    except ImportError as e:
        print(f"✗ Langchain Google GenAI failed: {e}")
        raise

    try:
        import newsapi
        print(f"✓ NewsAPI installed")
    except ImportError as e:
        print(f"✗ NewsAPI failed: {e}")
        raise

    try:
        import tavily
        print(f"✓ Tavily installed")
    except ImportError as e:
        print(f"✗ Tavily failed: {e}")
        raise

    try:
        import feedparser
        print(f"✓ Feedparser installed")
    except ImportError as e:
        print(f"✗ Feedparser failed: {e}")
        raise

def test_environment():
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    required_keys = ["GEMINI_API_KEY", "NEWSAPI_KEY", "TAVILY_API_KEY", "PERPLEXITY_API_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    
    if missing:
        print(f"✗ Missing API keys in .env: {missing}")
        raise ValueError(f"Missing API keys: {missing}")
    else:
        print(f"✓ All API keys present in .env")

if __name__ == "__main__":
    print("=== Phase 1 Setup Verification ===\n")
    test_python_version()
    test_imports()
    test_environment()
    print("\n✓ Phase 1 Setup Complete!")

