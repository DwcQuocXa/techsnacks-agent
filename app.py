import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path

from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState
from src.techsnack.config import settings

st.set_page_config(page_title="TechSnack AI Generator", page_icon="📰")
st.title("🇻🇳 TechSnack AI Generator")

@st.cache_resource
def get_graph():
    return create_techsnack_graph()

graph = get_graph()

tab1, tab2 = st.tabs(["🤖 Auto Generate", "✏️ Manual Topic"])

with tab1:
    st.subheader("Auto-Generate Today's TechSnack")
    if st.button("Generate Today's TechSnack", type="primary"):
        with st.spinner("Working..."):
            initial_state = TechSnackState(mode="auto", started_at=datetime.now())
            result = asyncio.run(graph.ainvoke(initial_state))
            
            st.success("✅ Article Generated!")
            st.metric("Topic", result.selected_topic)
            st.markdown("### 📝 Article")
            st.markdown(result.article)
            
            filename = f"techsnack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / filename
            output_path.write_text(result.article)
            
            st.download_button("⬇️ Download", result.article, filename)

with tab2:
    st.subheader("Generate from Custom Topic")
    topic_input = st.text_area("Enter topic:", height=100)
    
    if st.button("Research & Generate", type="primary", disabled=not topic_input):
        with st.spinner(f"Researching..."):
            initial_state = TechSnackState(mode="manual", user_topic=topic_input, started_at=datetime.now())
            result = asyncio.run(graph.ainvoke(initial_state))
            
            st.success("✅ Article Generated!")
            st.markdown(result.article)
            
            filename = f"techsnack_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_dir = Path(settings.output_dir)
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / filename
            output_path.write_text(result.article)
            
            st.download_button("⬇️ Download", result.article, filename)

