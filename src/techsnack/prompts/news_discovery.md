Today is {{date}}.

# Audience
Software engineers, tech leaders, and AI startup founders seeking actionable daily TechSnack topics.

# Context
You are analyzing today's most relevant tech headlines:

{{headlines}}

# Topic Categories (Priority Order)
Focus on news that impacts developers and tech professionals:

1. **AI & ML Breakthroughs** - New models, capabilities, or research that changes the game
2. **Developer Tools & Platforms** - New tools, frameworks, SDKs, or major updates
3. **Big Tech Moves** - Product launches, strategic shifts, acquisitions, or pivots by FAANG/major tech companies
4. **Tech Leadership & Vision** - CEOs/CTOs making bold predictions, controversial statements, or announcing major directions
5. **Industry Disruption** - Startups raising significant funding, new unicorns, or companies entering new markets
6. **Engineering Culture & Careers** - Layoffs, hiring freezes, return-to-office mandates, compensation trends
7. **Infrastructure & Cloud** - Major outages, new services, pricing changes, or architectural innovations
8. **Open Source Wins** - Significant releases, community milestones, or licensing changes
9. **Security & Privacy** - Critical vulnerabilities, breaches, or new regulations affecting developers
10. **Future Tech Trends** - Emerging technologies gaining traction (Web3, quantum, edge computing, etc.)

# Selection Criteria
Rate each topic on **fame_score (0-10)** based on:
- **Impact**: Will this affect developers' daily work or career decisions?
- **Timeliness**: Is this breaking news or a hot trending topic right now?
- **Practicality**: Can engineers learn something actionable or form an opinion?
- **Buzz**: Is the tech community actively discussing this on X/Twitter, HN, Reddit?

# Examples of Great TechSnack Topics

**Example 1: AI Model Launch**
- Topic: "OpenAI releases GPT-5 with native code execution and 10M context window"
- Why: Developers can immediately experiment, changes how AI coding assistants work
- Fame Score: 10/10
- Category: AI & ML Breakthroughs

**Example 2: Developer Tool**
- Topic: "Vercel announces v0.dev AI-powered UI generator going open source"
- Why: Frontend devs can use it for rapid prototyping, challenges traditional workflows
- Fame Score: 8/10
- Category: Developer Tools & Platforms

**Example 3: Big Tech News**
- Topic: "Google Cloud suffers 4-hour global outage affecting Firebase and Cloud Run"
- Why: Engineers need to know about infrastructure reliability for architecture decisions
- Fame Score: 9/10
- Category: Infrastructure & Cloud

**Example 4: Leadership Statement**
- Topic: "Meta's Mark Zuckerberg: 'Open source will win the AI war' - commits $10B to Llama 4"
- Why: Signals industry direction, affects startup AI strategy and model selection
- Fame Score: 9/10
- Category: Tech Leadership & Vision

**Example 5: Industry Impact**
- Topic: "Amazon announces 15,000 engineering layoffs amid AWS slowdown"
- Why: Affects job market, hiring trends, and cloud industry outlook
- Fame Score: 8/10
- Category: Engineering Culture & Careers

**Example 6: Tool Update**
- Topic: "GitHub Copilot Workspace launches: AI builds entire features from issues"
- Why: Changes developer workflow, potential productivity multiplier
- Fame Score: 9/10
- Category: Developer Tools & Platforms

# Instructions
1. Analyze the provided headlines
2. Identify 3-5 candidate topics that fit the categories above
3. Prioritize topics with highest relevance to developers/engineers/founders
4. For each topic:
   - Write a clear, specific topic title (not just company name)
   - Explain why it matters RIGHT NOW for engineers
   - Assign a fame_score (0-10) based on selection criteria
   - Include at least one credible source URL
5. Rank topics by fame_score (highest first)

# Output Format
Return STRICT JSON with this structure:

{
  "today_topics": [
    {
      "topic": "Specific, actionable topic title",
      "reason": "Why this matters to developers/engineers right now - be specific about impact",
      "fame_score": 0-10,
      "category": "One of the 10 categories listed above",
      "sources": ["https://credible-source.com/article"]
    }
  ]
}

# Quality Checklist
- [ ] Each topic is specific and actionable (not vague like "AI advances")
- [ ] Reasons explain practical impact on engineers' work or decisions
- [ ] Fame scores are justified (breaking news/high impact = 9-10, interesting but niche = 6-7)
- [ ] Sources are from credible tech media (TechCrunch, The Verge, Ars Technica, official blogs)
- [ ] Mix of categories when possible (not all AI news)

