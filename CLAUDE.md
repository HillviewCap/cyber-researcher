# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Package Management
- **Install dependencies**: `uv sync`
- **Install with dev dependencies**: `uv sync --dev`
- **Add new dependency**: `uv add <package>`
- **Add dev dependency**: `uv add --dev <package>`

### Code Quality
- **Format code**: `uv run black .`
- **Lint code**: `uv run ruff check .`
- **Type check**: `uv run mypy src/`
- **Run all quality checks**: `uv run black . && uv run ruff check . && uv run mypy src/`

### Testing
- **Run all tests**: `uv run pytest`
- **Run tests with verbose output**: `uv run pytest -v`
- **Run specific test file**: `uv run pytest tests/test_agents.py`
- **Run automated test runner**: `uv run python tests/run_tests.py`
- **Run tests with coverage**: `uv run pytest --cov=src`

### Usage
- **Basic example**: `uv run python examples/basic_usage.py`
- **STORM with Claude**: `uv run python examples/storm_examples/run_storm_wiki_claude.py --output-dir output --retriever serper --do-research --do-generate-outline --do-generate-article --do-polish-article`
- **STORM with GPT**: `uv run python examples/storm_examples/run_storm_wiki_gpt.py --output-dir output --retriever serper --do-research --do-generate-outline --do-generate-article --do-polish-article`

## Architecture Overview

**Cyber-Researcher** is a narrative-focused cybersecurity research assistant built on Stanford's STORM framework. It generates educational content by blending historical narratives with technical cybersecurity concepts.

### Core Components

**Multi-Agent System**:
- `SecurityAnalystAgent` - Defensive security analysis
- `ThreatResearcherAgent` - Threat intelligence research  
- `HistorianAgent` - Historical context and narrative generation

**Main Orchestration**:
- `CyberStormRunner` - Primary API class that coordinates all agents and modules
- Located in `src/cyber_storm/runner.py`

**Retrieval Modules**:
- `ThreatIntelRM` - Vector-based retrieval for threat intelligence reports
- `HistoricalRM` - Specialized retrieval for historical events
- Located in `src/cyber_storm/rm/`

**Professional Content Templates**:
- `BlogPostTemplate` - Rich blog formatting with educational enhancements
- `BookChapterTemplate` - Structured chapters with learning objectives and assessments
- `ResearchReportTemplate` - Professional cybersecurity reports with metadata
- Located in `src/cyber_storm/templates/`

**Educational Content Modules**:
- `EducationalFormatter` - Advanced pedagogical formatting with learning scaffolding
- `AssessmentGenerator` - Comprehensive assessment creation (8+ question types)
- `InteractiveElementsGenerator` - Interactive learning elements (simulations, labs, gamification)
- Located in `src/cyber_storm/modules/`

**Configuration**:
- `CyberStormConfig` - Centralized configuration management
- Uses `secrets.toml` for API keys (gitignored)
- Located in `src/cyber_storm/config/`

### Data Flow
```
User Input → CyberStormRunner → Multi-Agent Discourse → Retrieval Modules → Template-Based Synthesis → Educational Enhancement → Output Generation
```

### Key Entry Points
- **Main API**: `CyberStormRunner` class
- **Configuration**: `CyberStormConfig` class  
- **Basic usage**: `examples/basic_usage.py`
- **STORM integration**: `examples/storm_examples/`

### Project Structure
```
src/cyber_storm/           # Main package
├── agents/               # Custom agent implementations
├── rm/                   # Retrieval modules (ThreatIntelRM, HistoricalRM)
├── config/               # Configuration management
├── templates/            # Professional content templates (blog, chapter, report)
├── modules/              # Educational content modules (formatter, assessments, interactive)
├── runner.py             # Main orchestration class
└── __init__.py          # Package initialization

tests/                    # Comprehensive test suite
├── test_agents.py        # Agent unit tests
├── test_retrieval.py     # Retrieval module tests
├── test_integration.py   # Integration tests
├── test_sample_data.py   # Real-world data tests
├── test_config.py        # Configuration tests
├── conftest.py          # Shared test fixtures
└── run_tests.py         # Automated test runner
```

### Output Formats
- **Blog Posts**: Educational cybersecurity content with historical context, enhanced with interactive elements
- **Book Chapters**: Structured educational material with learning objectives, exercises, and assessments
- **Research Reports**: Professional cybersecurity analysis reports with executive summaries and metadata
- **Interactive Sessions**: Co-STORM collaborative research sessions
- **Educational Content**: Enhanced formatting with scaffolding, knowledge checks, and progress tracking
- **Assessments**: Comprehensive evaluations with 8+ question types (multiple choice, scenarios, practicals)
- **Interactive Elements**: 8 types including simulations, virtual labs, decision trees, and gamification

### Requirements
- **Python 3.11+** required
- **API Keys**: Anthropic API key required in `secrets.toml` (Claude models are now default)
- **Search API**: Serper API key recommended (2500 free queries/month)
- **Optional**: OpenAI API key for fallback, Bing Search API for web retrieval, Qdrant for cloud vector store

### Configuration Files
- `secrets.toml` - API keys and sensitive configuration (gitignored)
- `pyproject.toml` - Project dependencies and tool configuration
- Uses TOML format for all configuration management

### Language Model Integration
- **Primary LLM**: Claude models (Anthropic) - integrated as default
  - Security Analyst: `claude-3-sonnet-20240229`
  - Threat Researcher: `claude-3-sonnet-20240229` 
  - Historian: `claude-3-opus-20240229`
- **Embeddings**: Hugging Face BAAI/bge-m3 model (default)
- **Search Engine**: Serper.dev (recommended), with fallback to Bing, DuckDuckGo, etc.
- **Fallback**: OpenAI GPT models available for compatibility

### Development Notes
- **Git Workflow**: Create feature branches from DEVELOPMENT, merge when tasks complete
- **Testing**: Comprehensive test suite with 89 tests covering agents, retrieval, integration, and sample data
- **Code Style**: Black formatting (line-length 100), Ruff linting, MyPy type checking
- **Error Handling**: Check for missing API keys and configuration issues on startup
- **Quality Assurance**: All modules validated through automated testing and manual verification

### Implementation Status
- ✅ **Phase 1**: Project Foundation & Setup (Complete)
- ✅ **Phase 2**: Base Implementation with Claude integration (Complete)
- ✅ **Phase 3**: Narrative Features & Professional Templates (Complete)
  - Professional content templates (blog, chapter, research report)
  - Educational content modules (formatter, assessments, interactive elements)
  - Enhanced CyberStormRunner with template integration
- ✅ **Phase 4**: Testing & Refinement (Complete)
  - Comprehensive test suite with 89 tests
  - Code quality enforcement (Black, Ruff, MyPy)
  - Manual validation of all new modules
- 🔄 **Phase 5**: Co-STORM Integration (Pending)
  - Collaborative discourse protocol implementation
- 📋 **Phase 6**: Example Generation (Pending)
  - Comprehensive example content across cybersecurity topics

### Core Features Implemented
- ✅ Multi-agent system with specialized cybersecurity agents
- ✅ Vector-based retrieval for threat intelligence and historical context
- ✅ Configuration management with TOML-based secrets handling
- ✅ Professional content templates with educational enhancements
- ✅ Interactive learning elements and comprehensive assessments
- ✅ Automated testing infrastructure and quality assurance