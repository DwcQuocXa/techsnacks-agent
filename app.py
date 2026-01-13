import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path

from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState
from src.techsnack.config import settings
from src.techsnack.logging_config import setup_logging

setup_logging()

st.set_page_config(page_title="TechSnack AI Generator", page_icon="📰", layout="wide")
st.title("🇻🇳 TechSnack AI Generator")

st.sidebar.header("⚙️ Settings")
writer_model = st.sidebar.selectbox(
    "Writer Model",
    ["gemini-3-flash-preview", "gemini-3-pro-preview"],
    index=0
)

def get_field(result, field):
    return result.get(field) if isinstance(result, dict) else getattr(result, field, None)

def show_pipeline_details(result):
    st.subheader("🔬 Pipeline Details")
    
    with st.expander("📰 News Fetcher", expanded=False):
        raw_news = get_field(result, "raw_news") or []
        if raw_news:
            st.write(f"**{len(raw_news)} news items fetched**")
            for i, item in enumerate(raw_news[:10], 1):
                title = item.get("title") if isinstance(item, dict) else getattr(item, "title", "Untitled")
                source = item.get("source") if isinstance(item, dict) else getattr(item, "source", "")
                st.write(f"{i}. {title} ({source})")
        else:
            st.write("No news fetched (manual mode)")
    
    with st.expander("🎯 Topic Selector", expanded=False):
        today_topics = get_field(result, "today_topics") or []
        selected = get_field(result, "selected_topic")
        reasoning = get_field(result, "selection_reasoning")
        
        if today_topics:
            st.write(f"**{len(today_topics)} candidate topics:**")
            for t in today_topics[:5]:
                topic_name = t.get("topic", "Unknown") if isinstance(t, dict) else str(t)
                st.write(f"• {topic_name}")
        
        if selected:
            st.success(f"**Selected:** {selected}")
        if reasoning:
            st.info(f"**Reasoning:** {reasoning}")
    
    with st.expander("🧠 Planner", expanded=False):
        plan_topic = get_field(result, "plan_topic")
        queries = get_field(result, "plan_search_queries") or []
        
        if plan_topic:
            st.write(f"**Plan Topic:** {plan_topic}")
        if queries:
            st.write(f"**Search Queries ({len(queries)}):**")
            for q in queries:
                st.code(q, language=None)
    
    with st.expander("🔍 Researcher", expanded=False):
        research = get_field(result, "research_data")
        if research:
            sources = research.sources if hasattr(research, "sources") else research.get("sources", [])
            context = research.context if hasattr(research, "context") else research.get("context", "")
            
            if sources:
                st.write(f"**{len(sources)} sources found:**")
                for src in sources[:5]:
                    title = src.get("title", "Untitled")
                    url = src.get("url", "")
                    engine = src.get("source_engine", "")
                    st.write(f"• [{title}]({url}) ({engine})")
            
            if context:
                st.write("**Research Context:**")
                st.markdown(context)
        else:
            st.write("No research data")
    
    with st.expander("📊 Article Metadata", expanded=False):
        metadata = get_field(result, "article_metadata") or {}
        if metadata:
            cols = st.columns(3)
            cols[0].metric("Words", metadata.get("word_count", "N/A"))
            cols[1].metric("Model", metadata.get("model", "N/A"))
            started = get_field(result, "started_at")
            completed = get_field(result, "completed_at")
            if started and completed:
                duration = (completed - started).total_seconds()
                cols[2].metric("Duration", f"{duration:.1f}s")

@st.cache_resource
def get_graph():
    return create_techsnack_graph()

graph = get_graph()

tab1, tab2 = st.tabs(["🤖 Auto Generate", "✏️ Manual Topic"])

with tab1:
    st.subheader("Auto-Generate Today's TechSnack")
    if st.button("Generate Today's TechSnack", type="primary"):
        with st.spinner("🔍 Fetching news and generating article..."):
            initial_state = TechSnackState(mode="auto", writer_model=writer_model, started_at=datetime.now())
            result = asyncio.run(graph.ainvoke(initial_state))
        
        article = get_field(result, "article")
        selected_topic = get_field(result, "selected_topic")
        
        if article:
            st.success(f"✅ Generated: **{selected_topic}**")
            
            show_pipeline_details(result)
            
            st.divider()
            st.subheader("📝 Generated Article")
            st.markdown(article)
            st.divider()
            
            filename = f"techsnack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            (output_dir / filename).write_text(article)
            
            st.download_button("⬇️ Download Markdown", article, filename, mime="text/markdown")
        else:
            st.error("Failed to generate article. Please try again.")

with tab2:
    st.subheader("Generate from Custom Topic")
    topic_input = st.text_area("Enter topic:", height=100)
    user_instructions = st.text_area(
        "Additional instructions (optional):",
        placeholder="e.g., Focus on practical examples, compare with alternatives...",
        height=80
    )
    
    if st.button("Research & Generate", type="primary", disabled=not topic_input):
        with st.spinner("🔍 Researching and generating article..."):
            initial_state = TechSnackState(
                mode="manual", 
                user_topic=topic_input, 
                user_query=user_instructions if user_instructions else None,
                writer_model=writer_model, 
                started_at=datetime.now()
            )
            result = asyncio.run(graph.ainvoke(initial_state))
        
        article = get_field(result, "article")
        
        if article:
            st.success(f"✅ Generated: **{topic_input}**")
            
            show_pipeline_details(result)
            
            st.divider()
            st.subheader("📝 Generated Article")
            st.markdown(article)
            st.divider()
            
            filename = f"techsnack_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            (output_dir / filename).write_text(article)
            
            st.download_button("⬇️ Download Markdown", article, filename, mime="text/markdown")
        else:
            st.error("Failed to generate article. Please try again.")

