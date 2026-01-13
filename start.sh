#!/bin/bash

# TechSnack AI - Start Script
# This script handles all setup and starts the Streamlit app

set -e  # Exit on error

echo "🇻🇳 TechSnack AI Generator - Starting..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version (3.11+ required)
echo "📋 Checking Python version..."
PYTHON_CMD=""
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python 3.11+ is required but not found${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found ($PYTHON_CMD)${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install/update dependencies
echo "📦 Installing dependencies..."
if command -v uv &> /dev/null; then
    uv pip install -e .
else
    pip install --upgrade pip
    pip install -e .
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from template..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}📝 Please edit .env and add your API keys:${NC}"
        echo "   Required:"
        echo "   - GEMINI_API_KEY"
        echo "   - PERPLEXITY_API_KEY"
        echo ""
        echo "   Optional (for additional features):"
        echo "   - NEWSAPI_KEY (news fetching)"
        echo "   - TAVILY_API_KEY (web search)"
        echo "   - OPENAI_API_KEY (alternative LLM)"
        echo ""
        echo -e "${YELLOW}Press Enter to continue after adding keys, or Ctrl+C to exit...${NC}"
        read -r
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
fi

# Verify API keys are set
echo "🔑 Checking API keys..."
source .env
missing_keys=()
optional_missing=()

# Required keys
if [ -z "$GEMINI_API_KEY" ]; then
    missing_keys+=("GEMINI_API_KEY")
fi
if [ -z "$PERPLEXITY_API_KEY" ]; then
    missing_keys+=("PERPLEXITY_API_KEY")
fi

# Optional keys (warn but don't fail)
if [ -z "$NEWSAPI_KEY" ]; then
    optional_missing+=("NEWSAPI_KEY")
fi
if [ -z "$TAVILY_API_KEY" ]; then
    optional_missing+=("TAVILY_API_KEY")
fi
if [ -z "$OPENAI_API_KEY" ]; then
    optional_missing+=("OPENAI_API_KEY")
fi

if [ ${#missing_keys[@]} -gt 0 ]; then
    echo -e "${RED}❌ Missing required API keys: ${missing_keys[*]}${NC}"
    echo "Please add them to .env file"
    exit 1
fi

echo -e "${GREEN}✓ Required API keys configured${NC}"

if [ ${#optional_missing[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Optional keys not set (some features disabled): ${optional_missing[*]}${NC}"
fi
echo ""

# Create outputs directory if it doesn't exist
if [ ! -d "outputs" ]; then
    mkdir -p outputs
    echo -e "${GREEN}✓ Created outputs directory${NC}"
    echo ""
fi

# Start Streamlit
echo "🚀 Starting TechSnack AI..."
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  TechSnack AI is starting...${NC}"
echo -e "${GREEN}  Open: http://localhost:8501${NC}"
echo -e "${GREEN}  Press Ctrl+C to stop${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

streamlit run app.py

