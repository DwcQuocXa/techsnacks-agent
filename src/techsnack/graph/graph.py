from langgraph.graph import StateGraph, END
from .state import TechSnackState
from .nodes import (
    news_fetcher_node,
    topic_selector_node,
    researcher_node,
    writer_node,
)
from ..logging_config import get_logger

logger = get_logger(__name__)

def route_after_input(state: TechSnackState) -> str:
    mode = "researcher" if state.mode == "manual" else "news_fetcher"
    logger.info(f"🚀 Starting TechSnack generation in {state.mode.upper()} mode")
    return mode

def create_techsnack_graph():
    workflow = StateGraph(TechSnackState)
    
    workflow.add_node("news_fetcher", news_fetcher_node)
    workflow.add_node("topic_selector", topic_selector_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    
    workflow.set_conditional_entry_point(route_after_input)
    workflow.add_edge("news_fetcher", "topic_selector")
    workflow.add_edge("topic_selector", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    return workflow.compile()

