from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts.prompts import get_writer_prompt, load_techsnack_examples
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)

async def writer_node(state: TechSnackState) -> TechSnackState:
    topic = state.selected_topic or state.user_topic
    logger.info(f"✍️  Writing TechSnack article about: {topic}")
    
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.7,
        max_output_tokens=2048,
        google_api_key=settings.gemini_api_key,
    )
    
    research_context = state.research_data.context if state.research_data else ""
    
    system_prompt = await get_writer_prompt()
    user_prompt = f"""
Topic: {topic}

Research Context:
{research_context}

Please write a TechSnack article following the style in the examples.
Target length: 1-2 minute read (~300-400 words in Vietnamese).
"""
    
    prompt_length = len(system_prompt + "\n\n" + examples + "\n" + user_prompt)
    logger.info(f"  📤 Gemini payload: model={settings.gemini_model}, temp=0.7, prompt_length={prompt_length}")
    logger.debug(f"  📤 Gemini topic: {topic}")
    
    logger.info("🤖 Generating article with Gemini...")
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
    
    word_count = state.article_metadata["word_count"]
    logger.info(f"✓ Article complete! {word_count} words")
    
    return state

