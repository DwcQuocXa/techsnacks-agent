from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from ..state import TechSnackState
from ...prompts.prompts import get_writer_prompt, load_techsnack_examples
from ...config import settings
from ...logging_config import get_logger

logger = get_logger(__name__)


async def writer_node(state: TechSnackState) -> TechSnackState:
    topic = state.plan_topic or state.selected_topic or state.user_topic
    logger.info(f"✍️  Writing TechSnack article about: {topic}")

    if state.writer_model.startswith("gemini"):
        llm = ChatGoogleGenerativeAI(
            model=state.writer_model,
            google_api_key=settings.gemini_api_key,
            temperature=0.7,
        )
        logger.info(f"  🤖 Using Gemini model: {state.writer_model}")
    else:
        llm = ChatOpenAI(
            model=state.writer_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )
        logger.info(f"  🤖 Using OpenAI model: {state.writer_model}")

    research_context = state.research_data.context if state.research_data else ""
    source_count = len(state.research_data.sources) if state.research_data else 0
    logger.info(
        "  📚 Writer context: %s sources, context length=%s chars",
        source_count,
        len(research_context),
    )
    if state.research_data and state.research_data.sources:
        preview = [
            f"{src.get('source_engine','?')} | {src.get('title','(untitled)')}"
            for src in state.research_data.sources[:5]
        ]
        logger.info("  🔎 Context sources preview: %s", "; ".join(preview))
    logger.info("  🧾 Full writer context:\n%s", research_context or "<empty>")
    examples = await load_techsnack_examples()

    system_prompt = "You are a Vietnamese tech content writer for TechSnack series - a tech education series for Viet Tech Community in Finland."

    user_prompt = await get_writer_prompt()
    
    user_instructions = ""
    if state.user_query:
        user_instructions = f"\n\nUser Instructions:\n{state.user_query}\n"
        logger.info(f"  📝 User instructions: {state.user_query}")
    
    context_prompt = f"""
Topic: {topic}
{user_instructions}
Research Context:
{research_context}

Please write a TechSnack article following the style in the examples.
Target length: 1-2 minute read (~300-400 words in Vietnamese).
"""

    prompt_length = len(
        system_prompt + user_prompt + "\n\n" + examples + "\n" + context_prompt
    )
    logger.info(
        f"  📤 LLM payload: model={state.writer_model}, temp=0.7, prompt_length={prompt_length}"
    )
    logger.info(f"  📤 Topic: {topic}")

    logger.info(f"🤖 Generating article with {state.writer_model}...")
    response = await llm.ainvoke(
        [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt + "\n\n" + examples + "\n\n" + context_prompt,
            },
        ]
    )

    article_content = response.content
    if isinstance(article_content, list):
        article_content = " ".join(str(part) for part in article_content)
    
    state.article = article_content
    state.article_metadata = {
        "topic": topic,
        "model": state.writer_model,
        "generated_at": datetime.now().isoformat(),
        "word_count": len(article_content.split()),
    }
    state.completed_at = datetime.now()

    word_count = state.article_metadata["word_count"]
    logger.info(f"✓ Article complete! {word_count} words")

    return state
