"""Test full graph execution."""
import asyncio
from datetime import datetime
from src.techsnack.graph.graph import create_techsnack_graph
from src.techsnack.graph.state import TechSnackState

async def test_manual_mode():
    print("Testing manual mode...")
    graph = create_techsnack_graph()
    
    initial_state = TechSnackState(
        mode="manual",
        user_topic="Vector databases for AI",
        started_at=datetime.now()
    )
    
    result = await graph.ainvoke(initial_state)
    print(f"✓ Manual mode complete")
    print(f"  Article length: {len(result.article)} chars")
    print(f"  Research sources: {len(result.research_data.sources)}")
    return result

async def test_auto_mode():
    print("Testing auto mode...")
    graph = create_techsnack_graph()
    
    initial_state = TechSnackState(
        mode="auto",
        started_at=datetime.now()
    )
    
    result = await graph.ainvoke(initial_state)
    print(f"✓ Auto mode complete")
    print(f"  Selected topic: {result.selected_topic}")
    print(f"  Article length: {len(result.article)} chars")
    return result

async def main():
    print("=== Phase 6 Graph Verification ===\n")
    await test_manual_mode()
    print()
    await test_auto_mode()
    print("\n✓ Full graph working!")

if __name__ == "__main__":
    asyncio.run(main())

