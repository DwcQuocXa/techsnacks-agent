import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path

from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState
from src.techsnack.config import settings
from src.techsnack.logging_config import setup_logging

setup_logging()

st.set_page_config(page_title="TechSnack AI Generator", page_icon="📰")
st.title("🇻🇳 TechSnack AI Generator")

st.sidebar.header("⚙️ Settings")
writer_model = st.sidebar.selectbox(
    "Writer Model",
    ["gpt-5", "gemini-2.5-flash-preview-09-2025", "gemini-3-pro-preview"],
    index=0
)

@st.cache_resource
def get_graph():
    return create_techsnack_graph()

graph = get_graph()

tab1, tab2 = st.tabs(["🤖 Auto Generate", "✏️ Manual Topic"])

with tab1:
    st.subheader("Auto-Generate Today's TechSnack")
    if st.button("Generate Today's TechSnack", type="primary"):
        with st.spinner("Working..."):
            initial_state = TechSnackState(mode="auto", writer_model=writer_model, started_at=datetime.now())
            result = asyncio.run(graph.ainvoke(initial_state))
            
            st.success("✅ Article Generated!")
            
            selected_topic = result.get("selected_topic") if isinstance(result, dict) else result.selected_topic
            article = result.get("article") if isinstance(result, dict) else result.article
            
            st.metric("Topic", selected_topic)
            st.markdown("### 📝 Article")
            st.markdown(article)
            
            filename = f"techsnack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / filename
            output_path.write_text(article)
            
            st.download_button("⬇️ Download", article, filename)

with tab2:
    st.subheader("Generate from Custom Topic")
    topic_input = st.text_area("Enter topic:", height=100)
    user_instructions = st.text_area(
        "Additional instructions (optional):",
        placeholder="e.g., Focus on practical examples, compare with alternatives, emphasize security aspects...",
        height=80
    )
    
    if st.button("Research & Generate", type="primary", disabled=not topic_input):
        with st.spinner(f"Researching..."):
            initial_state = TechSnackState(
                mode="manual", 
                user_topic=topic_input, 
                user_query=user_instructions if user_instructions else None,
                writer_model=writer_model, 
                started_at=datetime.now()
            )
            result = asyncio.run(graph.ainvoke(initial_state))
            
            st.success("✅ Article Generated!")
            
            article = result.get("article") if isinstance(result, dict) else result.article
            st.markdown(article)
            
            filename = f"techsnack_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / filename
            output_path.write_text(article)
            
            st.download_button("⬇️ Download", article, filename)

