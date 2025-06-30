# Cyber-Researcher Frontend

A modern React frontend for the Cyber-Researcher cybersecurity research assistant.

## Features

- **Research Configuration**: Input topic and content directions with configurable options
- **Output Format Selection**: Choose between Blog Post, Book Chapter, Research Report, or Interactive Session
- **Real-time Progress**: WebSocket-powered progress tracking with agent activity monitoring
- **Results Display**: Preview generated content with download options (Markdown, JSON, Text)
- **Professional UI**: Clean, responsive design with TailwindCSS

## Technology Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **TailwindCSS** for styling
- **Headless UI** for accessible components
- **Heroicons** for icons
- **Tanstack React Query** for API state management
- **Axios** for HTTP requests
- **WebSocket** for real-time updates

## Development Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open http://localhost:5173 in your browser

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000`. Make sure the backend is running before starting the frontend.

To start the backend:
```bash
cd ..
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Component Structure

- `ResearchForm.tsx` - Main form for configuring research parameters
- `ProgressTracker.tsx` - Real-time progress display with WebSocket connection
- `ResultDisplay.tsx` - Results viewer with tabbed content and download options
- `App.tsx` - Main application with state management and routing logic

## API Services

- `services/api.ts` - Axios-based API client for backend communication
- `hooks/useWebSocket.ts` - WebSocket hook for real-time progress updates
- `types/research.ts` - TypeScript type definitions for API models

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Environment Configuration

The frontend is configured to connect to:
- **API Base URL**: `http://localhost:8000/api`
- **WebSocket URL**: `ws://localhost:8000/api/ws`

These can be modified in `src/services/api.ts` and `src/hooks/useWebSocket.ts` for different environments.