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
- **Run tests**: `uv run pytest`
- **Run tests with async support**: `uv run pytest -v`
- **Run specific test**: `uv run pytest tests/test_specific.py`

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

**Configuration**:
- `CyberStormConfig` - Centralized configuration management
- Uses `secrets.toml` for API keys (gitignored)
- Located in `src/cyber_storm/config/`

### Data Flow
```
User Input → CyberStormRunner → Multi-Agent Discourse → Retrieval Modules → Content Synthesis → Output Generation
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
├── modules/              # Content generation modules
└── runner.py             # Main orchestration class
```

### Output Formats
- **Blog Posts**: Educational cybersecurity content with historical context
- **Book Chapters**: Structured educational material with exercises
- **Interactive Sessions**: Co-STORM collaborative research sessions

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
- **Testing**: No automated tests yet - validate manually using examples
- **Code Style**: Black formatting (line-length 100), Ruff linting, MyPy type checking
- **Error Handling**: Check for missing API keys and configuration issues on startup

### Recent Updates
- ✅ Claude integration completed (Phase 2)
- ✅ Multi-agent system with specialized cybersecurity agents
- ✅ Vector-based retrieval for threat intelligence and historical context
- ✅ Configuration management with TOML-based secrets handling