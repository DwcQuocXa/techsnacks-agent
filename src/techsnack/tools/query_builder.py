from datetime import datetime

def build_news_discovery_query() -> str:
    """
    Build sophisticated query for discovering today's best tech news.
    Used in AUTO mode for finding trending topics.
    """
    today = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")
    
    return f"""Today is {day_of_week}, {today}.

Give me the most interesting and impactful tech and AI news from TODAY and this week that would excite software engineers and developers.

Focus specifically on:

**Breaking News & Major Announcements:**
- Product launches from Big Tech (Google, Microsoft, Meta, Apple, Amazon, OpenAI, Anthropic)
- New AI models, APIs, or developer tools released
- Major funding rounds for AI/tech startups
- Significant acquisitions or partnerships

**Industry Insights:**
- Statements from tech leaders and AI startup founders about emerging trends
- New research papers or breakthroughs (especially from labs like DeepMind, OpenAI Research)
- Shifts in tech industry direction or strategy

**Developer-Relevant News:**
- New programming languages, frameworks, or major version releases
- Developer tool announcements (IDEs, AI coding assistants, deployment platforms)
- Open source project milestones

**Business & Market:**
- Tech company layoffs or hiring freezes
- IPO announcements or significant market moves
- Regulatory changes affecting tech/AI

Prioritize news that:
- Is actionable or directly relevant to developers
- Represents significant technical innovation
- Has widespread industry impact
- Would spark interesting technical discussions

Provide concise summaries with sources."""

def build_topic_research_query(topic: str) -> str:
    """
    Build detailed research query for a specific topic.
    Used in both AUTO (after topic selection) and MANUAL modes.
    """
    today = datetime.now().strftime("%B %d, %Y")
    
    return f"""Today's date: {today}

Research this topic in depth for a Vietnamese tech article aimed at software developers:

**Topic:** {topic}

**Research Focus:**

1. **What it is & Why it matters now:**
   - Clear explanation of the concept/technology
   - Why is it relevant or trending TODAY
   - Recent developments or announcements (within last few weeks)

2. **Technical Details for Developers:**
   - How it actually works (architecture, key concepts)
   - Practical use cases and real-world applications
   - Code examples or implementation patterns if applicable

3. **Industry Context:**
   - Which companies/projects are using this
   - What problems does it solve
   - Comparisons with alternatives or related technologies

4. **Developer Perspective:**
   - How can developers use/adopt this
   - Skills or tools needed to get started
   - Potential career/learning opportunities

5. **Critical Analysis:**
   - Current limitations or challenges
   - Best practices and anti-patterns
   - Where the technology is heading

Provide detailed, accurate information with credible sources. Focus on practical insights that developers can apply."""

def build_quick_lookup_query(topic: str) -> str:
    """
    Build quick verification query for Tavily.
    Fast, broad search for supplementary information.
    """
    return f"{topic} latest news updates developer guide tutorial"

