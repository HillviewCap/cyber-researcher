# Cyber-Researcher

A narrative-focused cybersecurity research assistant that helps create educational content by blending historical stories with cybersecurity concepts, grounded in real threat intelligence reports.

## Overview

Cyber-Researcher leverages the STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking) framework to generate engaging cybersecurity educational content. It combines technical accuracy with historical storytelling to make complex security concepts accessible and memorable.

## Features

- **Multi-Agent Collaboration**: Simulates conversations between Security Analyst, Threat Researcher, and Historian agents
- **Threat Intelligence Integration**: Ingests and analyzes real threat intelligence reports
- **Historical Context**: Draws parallels between historical events and modern cyber incidents
- **Narrative Generation**: Creates blog posts and book chapters with engaging storytelling
- **Grounded Research**: All content is backed by citations and sources

## Installation

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cyber-researcher.git
cd cyber-researcher
```

2. Install dependencies with UV:
```bash
uv sync
```

3. Create a `secrets.toml` file in the root directory:
```toml
# API Keys
OPENAI_API_KEY = "your-openai-api-key"
BING_SEARCH_API_KEY = "your-bing-search-api-key"  # Optional, for web search

# Optional: For cloud vector store
QDRANT_API_KEY = "your-qdrant-api-key"
```

## Quick Start

### Generate a Blog Post

```python
from cyber_storm import CyberStormRunner

# Initialize the runner
runner = CyberStormRunner()

# Generate a blog post
blog_post = runner.generate_blog_post(
    topic="The evolution of ransomware: From PC Cyborg to modern attacks",
    style="educational"
)

print(blog_post.content)
```

### Interactive Research Session

```python
# Start an interactive Co-STORM session
session = runner.interactive_research(
    topic="Nation-state cyber operations and historical espionage parallels"
)

# The agents will collaborate to explore the topic
# You can observe or inject your own questions
```

## Project Structure

```
cyber-researcher/
   src/cyber_storm/       # Main package
      agents/           # Custom agent implementations
      modules/          # STORM modules for narrative generation
      rm/              # Retrieval modules
   data/                # Data storage
      threat_intel/    # Threat intelligence reports
      historical/      # Historical context database
   examples/            # Example usage scripts
   tests/              # Test suite
```

## Documentation

- [Architecture Document](ARCHITECTURE.md) - Detailed system design and components
- [API Reference](docs/api.md) - Complete API documentation
- [Examples](examples/) - Sample code and use cases

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on the [STORM framework](https://github.com/stanford-oval/storm) by Stanford University
- Inspired by the need for engaging cybersecurity education

## Status

This project is in active development. See the [Architecture Document](ARCHITECTURE.md) for the current implementation status and roadmap.