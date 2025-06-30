# Cyber-Researcher Architecture Document

## Project Overview
A narrative-focused cybersecurity research assistant that helps create educational content by blending historical stories with cybersecurity concepts, grounded in real threat intelligence reports. Built on the STORM research framework.

## Project Status Tracker

### Phase 1: Environment Setup ✅
- [x] Initialize UV project
- [x] Set up Git repository
- [x] Install core dependencies (knowledge-storm, openai, qdrant-client)
- [x] Create project structure
- [x] Configure secrets management

### Phase 2: Base Implementation ✅
- [x] Create custom agent classes
  - [x] Security Analyst Agent
  - [x] Threat Researcher Agent  
  - [x] Historian Agent
- [x] Implement threat intelligence retrieval module
- [x] Set up vector store for threat reports
- [x] Create historical context database
- [x] Implement main CyberStormRunner class
- [x] Create example usage script

### Phase 3: Narrative Features 🔲
- [x] Implement narrative generation module (basic)
- [ ] Create blog/book templates
- [x] Add historical parallel finder
- [x] Integrate storytelling elements (basic)
- [ ] Develop educational content formatter
- [ ] Add interactive Co-STORM discourse

### Phase 4: Testing & Refinement 🔲
- [ ] Create test suite
- [ ] Test with sample threat reports
- [ ] Generate example blog posts
- [ ] Refine agent interactions
- [ ] Optimize for educational value

## Architecture Components

### 1. Core System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface                         │
│              (CLI / Web Interface)                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│                  CyberStormRunner                        │
│         (Main Orchestration Component)                   │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   Security   │ │   Threat    │ │  Historian  │
│   Analyst    │ │ Researcher  │ │    Agent    │
│    Agent     │ │    Agent    │ │             │
└──────────────┘ └─────────────┘ └─────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Retrieval & Knowledge Base                  │
├─────────────────────────────────────────────────────────┤
│  • Threat Intelligence DB  • Historical Context DB      │
│  • Web Search APIs        • Vector Store               │
└─────────────────────────────────────────────────────────┘
```

### 2. Data Flow

```mermaid
graph TD
    A[User Input: Topic] --> B[CyberStormRunner]
    B --> C[Agent Discourse]
    C --> D[Security Analyst]
    C --> E[Threat Researcher]
    C --> F[Historian]
    
    D --> G[Threat Intel Retrieval]
    E --> G
    F --> H[Historical Context Retrieval]
    
    G --> I[Vector Store]
    H --> I
    
    I --> J[Narrative Generator]
    J --> K[Blog/Book Output]
```

### 3. Module Specifications

#### 3.1 Custom Agents

**Security Analyst Agent**
- **Purpose**: Analyze technical aspects of cybersecurity incidents
- **Key Methods**:
  - `analyze_threat_report()`
  - `extract_technical_details()`
  - `provide_security_context()`
- **Integration**: Uses threat intelligence retrieval module

**Threat Researcher Agent**
- **Purpose**: Deep dive into attack methodologies and campaigns
- **Key Methods**:
  - `research_attack_pattern()`
  - `link_to_campaigns()`
  - `verify_technical_accuracy()`
- **Integration**: Cross-references multiple threat reports

**Historian Agent**
- **Purpose**: Provide historical context and storytelling elements
- **Key Methods**:
  - `find_historical_parallels()`
  - `suggest_narrative_framework()`
  - `enhance_with_storytelling()`
- **Integration**: Uses historical context database

#### 3.2 Retrieval Modules

**ThreatIntelRM (Threat Intelligence Retrieval Module)**
- Extends VectorRM for threat report specific features
- CSV Schema: `content | title | url | description | date | threat_type | severity | targets`
- Supports PDF parsing and extraction
- Implements threat-specific search strategies

**HistoricalRM (Historical Context Retrieval Module)**
- Custom retrieval for historical events and narratives
- Categorized by themes and time periods
- Supports analogy and parallel finding

#### 3.3 Generation Modules

**NarrativeGenerator**
- Extends STORM's article generation
- Implements blog and book specific formatting
- Integrates citations in reader-friendly format
- Balances technical accuracy with readability

**HistoricalContextModule**
- Identifies opportunities for historical integration
- Suggests narrative frameworks
- Ensures smooth blending of technical and historical content

### 4. Configuration Structure

```python
# config/cyber_storm_config.py
class CyberStormConfig:
    # Agent Configuration
    agent_config = {
        "security_analyst": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000,
            "perspective": "technical_security"
        },
        "threat_researcher": {
            "model": "gpt-4",
            "temperature": 0.8,
            "max_tokens": 1000,
            "perspective": "threat_intelligence"
        },
        "historian": {
            "model": "gpt-4",
            "temperature": 0.9,
            "max_tokens": 1000,
            "perspective": "historical_narrative"
        }
    }
    
    # Generation Configuration
    generation_config = {
        "blog": {
            "min_words": 1500,
            "max_words": 3000,
            "style": "conversational_educational",
            "include_summary": True
        },
        "book_chapter": {
            "min_words": 5000,
            "max_words": 10000,
            "style": "formal_educational",
            "include_exercises": True
        }
    }
    
    # Retrieval Configuration
    retrieval_config = {
        "threat_intel_sources": ["local_db", "web_search"],
        "historical_sources": ["curated_db", "web_search"],
        "max_sources_per_query": 10,
        "relevance_threshold": 0.7
    }
```

### 5. API Design

```python
# Main API Interface
class CyberStormRunner:
    def __init__(self, config: CyberStormConfig):
        """Initialize with configuration"""
        
    def generate_blog_post(self, topic: str, style: str = "educational") -> BlogPost:
        """Generate a blog post on the given topic"""
        
    def generate_book_chapter(self, topic: str, chapter_num: int, 
                            learning_objectives: List[str]) -> BookChapter:
        """Generate a book chapter with specified learning objectives"""
        
    def interactive_research(self, topic: str) -> InteractiveSession:
        """Start an interactive Co-STORM session"""
        
    def ingest_threat_report(self, report_path: str) -> bool:
        """Add a threat intelligence report to the knowledge base"""
        
    def add_historical_context(self, event: HistoricalEvent) -> bool:
        """Add historical context to the database"""
```

### 6. File Structure Details

```
cyber-researcher/
├── ARCHITECTURE.md          # This document
├── README.md               # Project overview and usage
├── pyproject.toml          # UV project configuration
├── .python-version         # Python version (3.11)
├── .gitignore             # Git ignore rules
├── secrets.toml           # API keys (not committed)
├── src/
│   └── cyber_storm/
│       ├── __init__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py              # Base agent class
│       │   ├── security_analyst.py   # Security analyst implementation
│       │   ├── threat_researcher.py  # Threat researcher implementation
│       │   └── historian.py          # Historian implementation
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── narrative_generator.py    # Blog/book generation
│       │   ├── historical_context.py     # Historical integration
│       │   └── threat_intel_processor.py # Threat report processing
│       ├── rm/
│       │   ├── __init__.py
│       │   ├── threat_intel_rm.py    # Threat intel retrieval
│       │   └── historical_rm.py      # Historical retrieval
│       ├── config/
│       │   ├── __init__.py
│       │   └── cyber_storm_config.py # Configuration classes
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── pdf_parser.py        # PDF parsing utilities
│       │   └── formatters.py        # Output formatting
│       └── runner.py                # Main runner implementation
├── examples/
│   ├── blog_generator.py           # Example blog generation
│   ├── book_chapter_generator.py   # Example chapter generation
│   └── interactive_session.py      # Interactive research example
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_modules.py
│   └── test_integration.py
├── data/
│   ├── threat_intel/              # Threat intelligence reports
│   │   └── .gitkeep
│   ├── historical/                # Historical references
│   │   └── historical_events.csv
│   └── templates/                 # Output templates
│       ├── blog_template.md
│       └── chapter_template.md
└── output/                        # Generated content
    └── .gitkeep
```

### 7. Development Milestones

#### Milestone 1: Foundation (Week 1-2)
- [x] Architecture document creation
- [ ] Project setup with UV and Git
- [ ] Basic project structure
- [ ] Core dependencies installation
- [ ] Initial configuration system

#### Milestone 2: Core Implementation (Week 3-4)
- [ ] Base agent implementations
- [ ] Basic retrieval modules
- [ ] Simple narrative generation
- [ ] Initial integration tests

#### Milestone 3: Advanced Features (Week 5-6)
- [ ] Historical parallel finding
- [ ] Advanced narrative techniques
- [ ] Blog/book formatters
- [ ] Interactive session support

#### Milestone 4: Polish & Testing (Week 7-8)
- [ ] Comprehensive test suite
- [ ] Documentation completion
- [ ] Example generation
- [ ] Performance optimization

### 8. Technical Decisions

#### Language Models
- **Primary**: GPT-4 for all agents (balance of quality and cost)
- **Alternative**: GPT-3.5 for development/testing
- **Future**: Support for open-source models (Llama, Mistral)

#### Vector Store
- **Primary**: Qdrant (local and cloud support)
- **Embedding Model**: OpenAI text-embedding-3-small
- **Chunking Strategy**: Semantic paragraphs with overlap

#### Search APIs
- **Primary**: Bing Search (good balance of cost and quality)
- **Secondary**: DuckDuckGo (privacy-focused, no API key)
- **Future**: Custom scraping for specific threat intel sources

### 9. Security Considerations

- API keys stored in `secrets.toml` (never committed)
- Threat reports sanitized before ingestion
- Output reviewed for sensitive information disclosure
- Rate limiting on API calls
- Local vector store option for sensitive data

### 10. Future Enhancements

- Web interface for easier interaction
- Integration with popular blogging platforms
- Automated threat report ingestion
- Multi-language support
- Collaborative editing features
- Real-time threat intelligence updates

## Current Implementation Status (Phase 2 Complete)

### ✅ Completed Components

**Core Infrastructure:**
- UV project setup with proper dependencies
- Git repository with remote at github.com/HillviewCap/cyber-researcher
- Complete project structure with modular architecture
- Configuration management system with secrets handling

**Agent System:**
- `BaseCyberAgent`: Abstract base class for all agents
- `SecurityAnalystAgent`: Defensive security analysis and technical recommendations
- `ThreatResearcherAgent`: Threat intelligence and adversary analysis
- `HistorianAgent`: Historical context and narrative generation
- Agent coordination and perspective-driven analysis

**Retrieval Modules:**
- `ThreatIntelRM`: Vector-based retrieval for threat intelligence reports
- `HistoricalRM`: Specialized retrieval for historical events and parallels
- Web search integration (Bing, DuckDuckGo, etc.)
- Qdrant vector store support (local and cloud)

**Content Generation:**
- `CyberStormRunner`: Main orchestration class
- Blog post generation with multi-agent synthesis
- Book chapter generation with learning objectives
- Interactive research session creation
- Basic narrative synthesis combining all agent perspectives

**Examples and Documentation:**
- Complete usage example (`examples/basic_usage.py`)
- Sample data generation for testing
- Configuration templates and secrets management
- Comprehensive architecture documentation

### 🔄 Next Steps (Phase 3)

1. **Enhanced Co-STORM Integration**: Implement proper Co-STORM collaborative discourse
2. **Advanced Templates**: Create professional blog and book chapter templates
3. **Educational Features**: Add exercises, quizzes, and interactive elements
4. **Content Formatters**: Improve output formatting for different publication formats
5. **Testing Suite**: Comprehensive testing of all components

### 🚀 Ready for Use

The system is now functional for basic cybersecurity narrative generation. Users can:
- Generate educational blog posts combining security, threat, and historical perspectives
- Create book chapters with learning objectives and structured content
- Start interactive research sessions with multi-agent question generation
- Ingest threat intelligence reports and historical context data

To get started, copy `secrets.toml.example` to `secrets.toml`, configure your API keys, and run `python examples/basic_usage.py`.

---

**Last Updated**: 2025-06-30
**Version**: 1.0.0  
**Status**: Phase 2 Complete - Ready for Testing