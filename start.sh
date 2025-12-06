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

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3.12 &> /dev/null; then
    echo -e "${RED}❌ Python 3.12 is required but not found${NC}"
    echo "Please install Python 3.12 or higher"
    exit 1
fi
echo -e "${GREEN}✓ Python 3.12 found${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.12 -m venv .venv
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
pip install --upgrade pip --quiet
pip install -e . --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from template..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}📝 Please edit .env and add your API keys:${NC}"
        echo "   - GEMINI_API_KEY"
        echo "   - NEWSAPI_KEY"
        echo "   - TAVILY_API_KEY"
        echo "   - PERPLEXITY_API_KEY"
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

if [ -z "$GEMINI_API_KEY" ]; then
    missing_keys+=("GEMINI_API_KEY")
fi
if [ -z "$NEWSAPI_KEY" ]; then
    missing_keys+=("NEWSAPI_KEY")
fi
if [ -z "$TAVILY_API_KEY" ]; then
    missing_keys+=("TAVILY_API_KEY")
fi
if [ -z "$PERPLEXITY_API_KEY" ]; then
    missing_keys+=("PERPLEXITY_API_KEY")
fi
if [ -z "$OPENAI_API_KEY" ]; then
    missing_keys+=("OPENAI_API_KEY")
fi

if [ ${#missing_keys[@]} -gt 0 ]; then
    echo -e "${RED}❌ Missing API keys: ${missing_keys[*]}${NC}"
    echo "Please add them to .env file"
    exit 1
fi

echo -e "${GREEN}✓ All API keys configured${NC}"
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

