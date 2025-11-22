from pathlib import Path
from datetime import datetime

PROMPTS_DIR = Path(__file__).parent

def load_prompt(filename: str) -> str:
    filepath = PROMPTS_DIR / filename
    return filepath.read_text() if filepath.exists() else ""

async def get_topic_selector_prompt() -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")
    return load_prompt("topic_selector.md").replace("{{date}}", today)

async def get_writer_prompt() -> str:
    return load_prompt("writer.md")

async def load_techsnack_examples() -> str:
    examples_dir = PROMPTS_DIR / "examples"
    examples = []
    for file in sorted(examples_dir.glob("*.md")):
        content = file.read_text()
        examples.append(f"=== Example: {file.stem} ===\n{content}\n")
    return "\n\n".join(examples)

