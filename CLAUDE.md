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

### Database Management
- **Initialize database**: `uv run alembic upgrade head`
- **Create migration**: `uv run alembic revision --autogenerate -m "description"`
- **Apply migrations**: `uv run alembic upgrade head`
- **Downgrade migration**: `uv run alembic downgrade -1`

### Application Startup
- **API Server**: `uv run python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8234`
- **Frontend Development**: `cd frontend && npm install && npm run dev`
- **Frontend Build**: `cd frontend && npm run build`
- **Frontend Lint**: `cd frontend && npm run lint`

### Example Usage
- **Basic example**: `uv run python examples/basic_usage.py`
- **STORM with Claude**: `uv run python examples/storm_examples/run_storm_wiki_claude.py --output-dir output --retriever serper --do-research --do-generate-outline --do-generate-article --do-polish-article`
- **STORM with GPT**: `uv run python examples/storm_examples/run_storm_wiki_gpt.py --output-dir output --retriever serper --do-research --do-generate-outline --do-generate-article --do-polish-article`

## Version Control

### Git Workflow
- **Primary Branch**: `main` - Production-ready code
- **Feature Branches**: Create feature branches from `main`, merge back when complete
- **Development Flow**: Create feature branches for new work, merge back to `main` after testing

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

**Workflow Tracking System**:
- `WorkflowTracker` - Comprehensive agent activity tracking and audit trail
- Records individual agent steps with timing, status, and metadata
- Separates final content from workflow/process information
- Provides real-time progress callbacks and performance metrics
- Located in `src/cyber_storm/workflow_tracker.py`

**Database Layer**:
- `SQLAlchemy` - ORM with async support for research metadata persistence
- `Alembic` - Database migration management
- SQLite for development, PostgreSQL support for production
- Located in `src/api/database/`

**API Server**:
- `FastAPI` - REST API server with comprehensive CRUD operations
- WebSocket support for real-time research progress tracking
- Database integration with persistence layer
- Located in `src/api/`

**Frontend Interface**:
- `React/TypeScript` - Complete research management interface
- Advanced markdown editing with live preview
- Search, filtering, and pagination for research results
- Real-time progress tracking and result display
- Located in `frontend/`

### Data Flow
```
Frontend Interface → FastAPI Endpoints → Database Services → CyberStormRunner → WorkflowTracker → Multi-Agent Discourse → Retrieval Modules → Template-Based Synthesis → Educational Enhancement → Workflow Metadata Separation → Database Persistence → Frontend Display
```

### Content vs Workflow Separation
The system implements a critical separation between final content and workflow metadata:

**Content Data** (displayed in Content tab):
- Final polished research output only
- Professional, publication-ready format
- No agent workflow or process information

**Workflow Metadata** (displayed in Metadata tab):
- Complete agent activity audit trail with timing and status
- Step-by-step generation process tracking
- Agent contribution summaries and performance metrics
- Error tracking and retry counts
- Real-time progress information

### API Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Database      │
│   Components    │◄──►│   Routers       │◄──►│   Services      │
│                 │    │                 │    │                 │
│ - ResultsList   │    │ - Research CRUD │    │ - SQLAlchemy    │
│ - MarkdownEdit  │    │ - WebSocket     │    │ - Alembic       │
│ - SearchFilter  │    │ - Progress      │    │ - Persistence   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Entry Points
- **Main API**: `CyberStormRunner` class
- **Configuration**: `CyberStormConfig` class  
- **Web API**: `src/api/main.py` - FastAPI server entry point
- **Frontend**: `frontend/src/App.tsx` - React application entry point
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

src/api/                  # FastAPI web server
├── main.py              # FastAPI application entry point
├── database/            # Database models and configuration
│   ├── models.py        # SQLAlchemy models for persistence
│   └── base.py          # Database configuration
├── routers/             # API route handlers
├── models/              # Pydantic data models
├── services/            # Business logic services
│   ├── database_service.py  # Database operations
│   └── runner_service.py    # Research execution
└── dependencies.py      # Dependency injection

frontend/                 # React/TypeScript web interface
├── src/
│   ├── components/      # React components
│   │   ├── MarkdownViewer.tsx      # Markdown rendering
│   │   ├── MarkdownEditor.tsx      # Markdown editing with preview
│   │   ├── ResearchResultsList.tsx # Results management
│   │   └── ResearchResultEditor.tsx # Result editing modal
│   ├── services/        # API integration
│   ├── hooks/           # React hooks (WebSocket, etc.)
│   └── types/           # TypeScript type definitions
├── package.json         # Node.js dependencies
├── vite.config.ts       # Vite build configuration
└── tsconfig.json        # TypeScript configuration

alembic/                 # Database migrations
├── versions/            # Migration scripts
└── env.py              # Migration environment

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

### Development Environment
- **Database URL**: `sqlite:///./cyber_researcher.db`
- **API Server**: `http://localhost:8234`
- **API Documentation**: `http://localhost:8234/docs` (Swagger UI)
- **Frontend**: `http://localhost:5173` (when running)
- **WebSocket**: `ws://localhost:8234/api/ws/research/{session_id}`

### Requirements
- **Python 3.11+** required
- **Node.js 18+** for frontend development
- **API Keys**: Anthropic API key required in `secrets.toml` (Claude models are now default)
- **Search API**: Serper API key recommended (2500 free queries/month)
- **Optional**: OpenAI API key for fallback, Bing Search API for web retrieval, Qdrant for cloud vector store

### Configuration Files
- `secrets.toml` - API keys and sensitive configuration (gitignored)
- `pyproject.toml` - Project dependencies and tool configuration
- `frontend/package.json` - Node.js dependencies and scripts
- `alembic.ini` - Database migration configuration
- Uses TOML format for all configuration management

### Workflow Tracking Architecture
The system includes sophisticated workflow tracking for transparency and debugging:

**WorkflowTracker Class**:
- Tracks individual agent activities with unique IDs
- Records timing, status, input/output data, and sources
- Supports activity states: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`
- Provides real-time progress callbacks

**Database Integration**:
- `AgentActivity` model stores complete activity records
- Activities linked to research sessions via foreign keys
- Comprehensive error tracking with retry support
- Performance metrics for optimization analysis

**Metadata Structure**:
- `workflow_metadata` - Complete workflow information and agent activities
- `generation_process` - Step-by-step process breakdown
- `agent_workflow_summary` - Agent contribution summaries
- `agent_contributions` - Legacy field for backward compatibility

### Language Model Integration
- **Primary LLM**: Claude models (Anthropic) - integrated as default
  - Security Analyst: `claude-3-sonnet-20240229`
  - Threat Researcher: `claude-3-sonnet-20240229` 
  - Historian: `claude-3-opus-20240229`
- **Embeddings**: Hugging Face BAAI/bge-m3 model (default)
- **Search Engine**: Serper.dev (recommended), with fallback to Bing, DuckDuckGo, etc.
- **Fallback**: OpenAI GPT models available for compatibility

### Development Notes
- **Git Workflow**: Create feature branches from `main`, merge when tasks complete
- **Testing**: Comprehensive test suite with 89 tests covering agents, retrieval, integration, and sample data
- **Code Style**: Black formatting (line-length 100), Ruff linting, MyPy type checking
- **Error Handling**: Check for missing API keys and configuration issues on startup
- **Quality Assurance**: All modules validated through automated testing and manual verification
- **Frontend**: React with TypeScript, Vite build system, TailwindCSS for styling
- **API**: FastAPI with WebSocket support for real-time communication

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
- ✅ **Phase 5**: Database & API Infrastructure (Complete)
  - SQLAlchemy ORM with async support
  - Alembic database migrations
  - FastAPI with comprehensive CRUD operations
  - WebSocket support for real-time updates
- ✅ **Phase 6**: Frontend Interface & Markdown Support (Complete)
  - Complete React/TypeScript interface
  - Advanced markdown editing with live preview
  - Research results management with search and filtering
  - Real-time progress tracking and WebSocket integration
- 🔄 **Phase 7**: Co-STORM Integration (Pending)
  - Collaborative discourse protocol implementation
- 📋 **Phase 8**: Example Generation (Pending)
  - Comprehensive example content across cybersecurity topics

### Core Features Implemented
- ✅ Multi-agent system with specialized cybersecurity agents
- ✅ Vector-based retrieval for threat intelligence and historical context
- ✅ Configuration management with TOML-based secrets handling
- ✅ Professional content templates with educational enhancements
- ✅ Interactive learning elements and comprehensive assessments
- ✅ Database persistence with research metadata storage
- ✅ Complete web interface with markdown editing capabilities
- ✅ Real-time progress tracking via WebSocket
- ✅ Automated testing infrastructure and quality assurance
- ✅ Workflow tracking and agent activity audit trail system
- ✅ Content/workflow metadata separation for clean presentation

## AI Agent Management
- **Create agents to complete independent tasks**

## Web Search Capabilities
- Use web search capability for recent documentation on:
  - API documentation
  - Git projects
  - AI concepts
  - Dependency versions

## Framework Guidance
- **STORM Framework Integration**:
  - This project utilizes the Stanford AI Storm Research Framework. Check for existing functionality within the library and framework before creating any new features.
  - The storm repository can be referenced here for additional documentation and modules references: https://github.com/stanford-oval/storm

## Development Workflow

### Full Stack Development
This is a full-stack application with both backend (Python/FastAPI) and frontend (React/TypeScript) components. Key considerations:

- **Database First**: Always run database migrations before starting the API server
- **API Port**: The API server runs on port 8234 (not 8000) to avoid conflicts
- **Frontend Integration**: The frontend expects the API at `http://localhost:8234`
- **Real-time Features**: WebSocket connections are used for progress tracking during research generation

### Debugging and Development
- **API Logs**: FastAPI provides detailed request/response logging
- **Database Inspection**: Use `cyber_researcher.db` with SQLite browser for debugging
- **Frontend DevTools**: React DevTools and browser console for frontend debugging
- **WebSocket Testing**: Use browser DevTools Network tab to monitor WebSocket connections

### Key Integration Points
- **Research Generation**: `CyberStormRunner` in `src/cyber_storm/runner.py` is the main orchestration point
- **Database Operations**: `DatabaseService` in `src/api/services/database_service.py` handles all persistence
- **Frontend State**: React components use TanStack Query for server state management
- **Markdown Processing**: Frontend uses `react-markdown` with syntax highlighting and GitHub-flavored markdown