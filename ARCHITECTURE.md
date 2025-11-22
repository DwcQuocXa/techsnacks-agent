# TechSnack AI - System Architecture

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI[Streamlit App]
    end
    
    subgraph "LangGraph Workflow"
        Entry{Entry Point<br/>Mode?}
        NF[News Fetcher<br/>Node]
        TS[Topic Selector<br/>Node]
        R[Researcher<br/>Node]
        W[Writer<br/>Node]
    end
    
    subgraph "External APIs"
        NewsAPI[NewsAPI]
        HN[HackerNews API]
        RSS[Google News RSS]
        Perplexity[Perplexity API]
        Tavily[Tavily API]
        Gemini[Gemini 2.0 Flash]
    end
    
    subgraph "Tools Layer"
        NFT[News Fetcher Tools]
        QB[Query Builder]
        PS[Perplexity Search]
        US[Unified Search]
    end
    
    UI -->|Auto Mode| Entry
    UI -->|Manual Mode<br/>+ Topic| Entry
    
    Entry -->|Auto| NF
    Entry -->|Manual| R
    
    NF --> NFT
    NFT --> NewsAPI
    NFT --> HN
    NFT --> RSS
    
    NF --> TS
    TS --> QB
    TS --> PS
    PS --> Perplexity
    TS --> Gemini
    
    TS --> R
    R --> QB
    R --> US
    US --> PS
    US --> Tavily
    
    R --> W
    W --> Gemini
    W -->|Article| UI
    
    style Entry fill:#f9f,stroke:#333,stroke-width:4px
    style Perplexity fill:#90EE90,stroke:#333,stroke-width:2px
    style Tavily fill:#87CEEB,stroke:#333,stroke-width:2px
    style Gemini fill:#FFD700,stroke:#333,stroke-width:2px
```

## Detailed Workflow - Auto Mode

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Graph as LangGraph
    participant NF as News Fetcher
    participant TS as Topic Selector
    participant R as Researcher
    participant W as Writer
    participant Perplexity
    participant Tavily
    participant Gemini
    
    User->>UI: Click "Generate Today's TechSnack"
    UI->>Graph: Initialize (mode=auto)
    
    Graph->>NF: Execute News Fetcher Node
    NF->>NF: Parallel fetch from NewsAPI, HN, RSS
    NF-->>Graph: raw_news[30+ items]
    
    Graph->>TS: Execute Topic Selector Node
    TS->>Perplexity: build_news_discovery_query()<br/>(Today's date + context)
    Perplexity-->>TS: Trending tech news summary + sources
    TS->>TS: Combine Perplexity + raw_news
    TS->>Gemini: Select best topic
    Gemini-->>TS: selected_topic + reasoning
    TS-->>Graph: selected_topic
    
    Graph->>R: Execute Researcher Node
    R->>R: build_topic_research_query(topic)
    
    par Parallel Search
        R->>Perplexity: Deep research query
        Perplexity-->>R: Detailed analysis + citations
    and
        R->>Tavily: Quick lookup query
        Tavily-->>R: Broad sources + snippets
    end
    
    R->>R: Combine results
    R-->>Graph: research_data (sources, context, details)
    
    Graph->>W: Execute Writer Node
    W->>W: Load prompts + examples
    W->>Gemini: Generate article (Vietnamese style)
    Gemini-->>W: article content
    W-->>Graph: article + metadata
    
    Graph-->>UI: Complete state
    UI->>UI: Display article + download
    UI-->>User: Show generated TechSnack
```

## Detailed Workflow - Manual Mode

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Graph as LangGraph
    participant R as Researcher
    participant W as Writer
    participant Perplexity
    participant Tavily
    participant Gemini
    
    User->>UI: Enter custom topic
    UI->>Graph: Initialize (mode=manual, user_topic)
    
    Graph->>R: Execute Researcher Node
    R->>R: build_topic_research_query(topic)<br/>(Date + 5 focus areas)
    
    par Parallel Search
        R->>Perplexity: Research query
        Perplexity-->>R: Deep analysis
    and
        R->>Tavily: Lookup query
        Tavily-->>R: Quick facts
    end
    
    R-->>Graph: research_data
    
    Graph->>W: Execute Writer Node
    W->>Gemini: Generate article
    Gemini-->>W: article
    W-->>Graph: Complete
    
    Graph-->>UI: article
    UI-->>User: Display + download
```

## Component Architecture

```mermaid
graph LR
    subgraph "Presentation Layer"
        ST[Streamlit UI<br/>app.py]
    end
    
    subgraph "Orchestration Layer"
        G[LangGraph Workflow<br/>graph.py]
        State[State Management<br/>state.py]
    end
    
    subgraph "Business Logic Layer"
        N1[News Fetcher<br/>Node]
        N2[Topic Selector<br/>Node]
        N3[Researcher<br/>Node]
        N4[Writer<br/>Node]
    end
    
    subgraph "Tools & Utilities"
        QB[Query Builder<br/>Date-aware queries]
        PS[Perplexity Search<br/>Deep analysis]
        TS[Tavily Search<br/>Quick lookup]
        US[Unified Search<br/>Combines both]
        NF[News Fetchers<br/>API integrations]
        PL[Prompt Loader<br/>Template management]
    end
    
    subgraph "Data Layer"
        Models[Pydantic Models<br/>NewsItem, ResearchData]
        Config[Configuration<br/>Settings, API keys]
    end
    
    ST --> G
    G --> State
    G --> N1
    G --> N2
    G --> N3
    G --> N4
    
    N1 --> NF
    N2 --> QB
    N2 --> PS
    N3 --> QB
    N3 --> US
    N4 --> PL
    
    US --> PS
    US --> TS
    
    N1 --> Models
    N2 --> Models
    N3 --> Models
    N4 --> Models
    
    QB --> Config
    PS --> Config
    TS --> Config
    NF --> Config
```

## Data Flow - Unified Search

```mermaid
graph TD
    Start[Query: Topic for Research]
    
    QB[Query Builder]
    QB1[build_topic_research_query]
    QB2[build_quick_lookup_query]
    
    Start --> QB
    QB --> QB1
    QB --> QB2
    
    QB1 --> |Sophisticated query<br/>Date + 5 focus areas| PS[Perplexity Search]
    QB2 --> |Simple query<br/>Latest updates| TS[Tavily Search]
    
    PS --> |Deep Analysis| PR[Perplexity Result]
    TS --> |Quick Facts| TR[Tavily Result]
    
    PR --> Combine[Unified Search<br/>Combines Results]
    TR --> Combine
    
    Combine --> Output{Output}
    
    Output --> Sources[Combined Sources<br/>with attribution]
    Output --> Context[Synthesized Context<br/>Perplexity + Tavily]
    Output --> Metadata[Metadata<br/>which engines used]
    
    style PS fill:#90EE90
    style TS fill:#87CEEB
    style Combine fill:#FFE4B5
```

## Query Builder Strategy

```mermaid
graph TB
    subgraph "Query Types"
        Q1[News Discovery Query]
        Q2[Topic Research Query]
        Q3[Quick Lookup Query]
    end
    
    subgraph "News Discovery<br/>(Auto Mode)"
        ND1[Today: date + day]
        ND2[Focus: Big Tech, AI, Tools]
        ND3[Target: Engineers]
        ND4[Include: Layoffs, Funding]
    end
    
    subgraph "Topic Research<br/>(Both Modes)"
        TR1[What it is & Why now]
        TR2[Technical Details]
        TR3[Industry Context]
        TR4[Developer Perspective]
        TR5[Critical Analysis]
    end
    
    subgraph "Quick Lookup<br/>(Tavily)"
        QL1[Simple keywords]
        QL2[Latest updates]
        QL3[Guides & tutorials]
    end
    
    Q1 --> ND1
    Q1 --> ND2
    Q1 --> ND3
    Q1 --> ND4
    
    Q2 --> TR1
    Q2 --> TR2
    Q2 --> TR3
    Q2 --> TR4
    Q2 --> TR5
    
    Q3 --> QL1
    Q3 --> QL2
    Q3 --> QL3
    
    style Q1 fill:#FFB6C1
    style Q2 fill:#98FB98
    style Q3 fill:#87CEEB
```

## Cost & Performance Profile

```mermaid
graph LR
    subgraph "Auto Mode - $1.00/article"
        AM1[News APIs<br/>FREE]
        AM2[Perplexity News Discovery<br/>$0.60<br/>~3K tokens]
        AM3[Perplexity Research<br/>$0.40<br/>~2K tokens]
        AM4[Tavily<br/>FREE<br/>1000/month]
        AM5[Gemini<br/>FREE<br/>generous tier]
    end
    
    subgraph "Manual Mode - $0.40/article"
        MM1[Perplexity Research<br/>$0.40<br/>~2K tokens]
        MM2[Tavily<br/>FREE]
        MM3[Gemini<br/>FREE]
    end
    
    subgraph "Performance"
        P1[Parallel Execution<br/>Perplexity + Tavily]
        P2[Async Operations<br/>News fetching]
        P3[Caching<br/>LangGraph state]
    end
    
    style AM2 fill:#FFE4B5
    style AM3 fill:#FFE4B5
    style MM1 fill:#FFE4B5
    style P1 fill:#90EE90
```

## File Structure

```
techsnacks-agent/
├── app.py                          # Streamlit UI entry point
│
├── src/techsnack/
│   ├── config.py                   # Settings & API keys
│   ├── models.py                   # NewsItem
│   │
│   ├── graph/
│   │   ├── graph.py               # LangGraph workflow
│   │   ├── state.py               # TechSnackState, ResearchData
│   │   └── nodes/
│   │       ├── news_fetcher_node.py      # Parallel news fetching
│   │       ├── topic_selector_node.py    # Perplexity discovery + LLM selection
│   │       ├── researcher_node.py        # Unified search (Perplexity + Tavily)
│   │       └── writer_node.py           # Article generation
│   │
│   ├── tools/
│   │   ├── query_builder.py       # 🆕 Smart, date-aware queries
│   │   ├── perplexity_search.py   # 🆕 Perplexity integration
│   │   ├── web_search.py          # 🆕 Unified search (both engines)
│   │   └── news_fetcher.py        # NewsAPI, HN, RSS
│   │
│   └── prompts/
│       ├── prompts.py             # Prompt loader
│       ├── topic_selector.md      # Selection criteria
│       ├── writer.md              # Vietnamese style guide
│       └── examples/              # Few-shot examples
│
└── tests/
    ├── test_setup.py              # Environment verification
    ├── test_tools.py              # API integrations
    ├── test_perplexity.py         # 🆕 Perplexity tests
    └── test_graph.py              # End-to-end workflow
```

## Key Design Decisions

### 1. **Dual Search Strategy**
- **Perplexity**: Deep, contextual analysis with citations
- **Tavily**: Fast, broad coverage with diverse sources
- **Together**: Best of both worlds

### 2. **Smart Query Builder**
- Date-aware queries for relevance
- Context-rich prompts for better results
- Different strategies for discovery vs research

### 3. **Parallel Execution**
- News fetching: All 3 sources in parallel
- Search: Perplexity + Tavily simultaneously
- Reduces total latency significantly

### 4. **No Feature Flags**
- Both search engines used by default
- Simpler configuration
- Better out-of-box experience

### 5. **Type Safety**
- Pydantic models throughout
- Clear data contracts between nodes
- Easy debugging and validation

---

**Legend:**
- 🆕 = New Perplexity integration components
- FREE = No cost APIs
- $ = Paid APIs with costs shown

