/**
 * Main App component for Cyber-Researcher frontend.
 */

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ResearchForm } from './components/ResearchForm';
import { ProgressTracker } from './components/ProgressTracker';
import { ResultDisplay } from './components/ResultDisplay';
import { ResearchResultsList } from './components/ResearchResultsList';
import { ResearchResultEditor } from './components/ResearchResultEditor';
import { useWebSocket } from './hooks/useWebSocket';
import { researchApi } from './services/api';
import type { 
  ResearchRequest, 
  ResearchResult, 
  ProgressUpdate 
} from './types/research';
import { ResearchStatus } from './types/research';
import { 
  ShieldCheckIcon, 
  BeakerIcon,
  DocumentTextIcon,
  PlusIcon,
  FolderOpenIcon
} from '@heroicons/react/24/outline';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

interface AppState {
  currentSessionId: string | null;
  currentResult: ResearchResult | null;
  isLoading: boolean;
  error: string | null;
  currentView: 'research' | 'results';
  selectedResult: ResearchResult | null;
  isEditing: boolean;
}

function AppContent() {
  const [state, setState] = useState<AppState>({
    currentSessionId: null,
    currentResult: null,
    isLoading: false,
    error: null,
    currentView: 'research',
    selectedResult: null,
    isEditing: false,
  });

  const [progressUpdate, setProgressUpdate] = useState<ProgressUpdate | null>(null);

  // WebSocket connection for real-time updates
  const { isConnected, error: wsError } = useWebSocket(
    state.currentSessionId,
    {
      onMessage: (update: ProgressUpdate) => {
        setProgressUpdate(update);
        
        // Check if research is completed
        if (update.status === ResearchStatus.COMPLETED && state.currentSessionId) {
          fetchResult(state.currentSessionId);
        } else if (update.status === ResearchStatus.FAILED) {
          setState(prev => ({
            ...prev,
            isLoading: false,
            error: 'Research failed. Please try again.',
          }));
        }
      },
      onError: (error) => {
        console.error('WebSocket error:', error);
      },
    }
  );

  const fetchResult = async (sessionId: string) => {
    try {
      const result = await researchApi.getResearchResult(sessionId);
      if (result) {
        setState(prev => ({
          ...prev,
          currentResult: result,
          isLoading: false,
        }));
      } else {
        // Result not ready yet, keep checking
        setState(prev => ({
          ...prev,
          isLoading: false,
        }));
      }
    } catch (error) {
      console.error('Failed to fetch result:', error);
      setState(prev => ({
        ...prev,
        error: 'Failed to fetch research result.',
        isLoading: false,
      }));
    }
  };

  const handleStartResearch = async (request: ResearchRequest) => {
    setState(prev => ({
      ...prev,
      isLoading: true,
      error: null,
      currentResult: null,
    }));
    setProgressUpdate(null);

    try {
      const response = await researchApi.startResearch(request);
      setState(prev => ({
        ...prev,
        currentSessionId: response.session_id,
      }));
    } catch (error) {
      console.error('Failed to start research:', error);
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: 'Failed to start research. Please check your connection and try again.',
      }));
    }
  };

  const handleDownload = (format: 'markdown' | 'json' | 'txt') => {
    if (!state.currentResult) return;

    let content: string;
    let filename: string;
    let mimeType: string;

    switch (format) {
      case 'markdown':
        content = state.currentResult.content;
        filename = `${state.currentResult.title.replace(/[^a-z0-9]/gi, '_')}.md`;
        mimeType = 'text/markdown';
        break;
      case 'json':
        content = JSON.stringify(state.currentResult, null, 2);
        filename = `${state.currentResult.title.replace(/[^a-z0-9]/gi, '_')}.json`;
        mimeType = 'application/json';
        break;
      case 'txt':
        content = state.currentResult.content;
        filename = `${state.currentResult.title.replace(/[^a-z0-9]/gi, '_')}.txt`;
        mimeType = 'text/plain';
        break;
      default:
        return;
    }

    // Create and trigger download
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleNewResearch = () => {
    setState({
      currentSessionId: null,
      currentResult: null,
      isLoading: false,
      error: null,
      currentView: 'research',
      selectedResult: null,
      isEditing: false,
    });
    setProgressUpdate(null);
  };

  // Navigation handlers
  const handleViewChange = (view: 'research' | 'results') => {
    setState(prev => ({
      ...prev,
      currentView: view,
      selectedResult: null,
      isEditing: false,
    }));
  };

  // Result management handlers
  const handleViewResult = (result: ResearchResult) => {
    setState(prev => ({
      ...prev,
      selectedResult: result,
      isEditing: false,
    }));
  };

  const handleEditResult = (result: ResearchResult) => {
    setState(prev => ({
      ...prev,
      selectedResult: result,
      isEditing: true,
    }));
  };

  const handleCloseResultEditor = () => {
    setState(prev => ({
      ...prev,
      selectedResult: null,
      isEditing: false,
    }));
  };

  const handleResultSaved = (updatedResult: ResearchResult) => {
    setState(prev => ({
      ...prev,
      selectedResult: updatedResult,
      isEditing: false,
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <ShieldCheckIcon className="h-8 w-8 text-cyber-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Cyber-Researcher</h1>
                <p className="text-sm text-gray-600">Narrative-focused cybersecurity research assistant</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-6">
              {/* Navigation Tabs */}
              <nav className="flex space-x-4">
                <button
                  onClick={() => handleViewChange('research')}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    state.currentView === 'research'
                      ? 'bg-cyber-100 text-cyber-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <PlusIcon className="h-4 w-4" />
                  <span>New Research</span>
                </button>
                <button
                  onClick={() => handleViewChange('results')}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    state.currentView === 'results'
                      ? 'bg-cyber-100 text-cyber-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <FolderOpenIcon className="h-4 w-4" />
                  <span>Research Results</span>
                </button>
              </nav>

              {/* Status Indicators */}
              <div className="flex items-center space-x-4 border-l border-gray-200 pl-6">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <BeakerIcon className="h-4 w-4" />
                  <span>Multi-Agent System</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <DocumentTextIcon className="h-4 w-4" />
                  <span>AI-Powered Research</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Display */}
        {state.error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex">
              <div className="text-sm text-red-600">{state.error}</div>
              <button
                onClick={() => setState(prev => ({ ...prev, error: null }))}
                className="ml-auto text-red-400 hover:text-red-600"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Research View */}
        {state.currentView === 'research' && (
          <>
            {/* Research Form */}
            {!state.currentSessionId && !state.currentResult && (
              <ResearchForm
                onSubmit={handleStartResearch}
                isLoading={state.isLoading}
              />
            )}

            {/* Progress Tracking */}
            {state.currentSessionId && !state.currentResult && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-gray-900">Research in Progress</h2>
                  <button
                    onClick={handleNewResearch}
                    className="btn-secondary"
                  >
                    Start New Research
                  </button>
                </div>
                
                <ProgressTracker
                  update={progressUpdate}
                  isConnected={isConnected}
                  error={wsError}
                />
              </div>
            )}

            {/* Results Display */}
            {state.currentResult && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-gray-900">Research Complete</h2>
                  <button
                    onClick={handleNewResearch}
                    className="btn-primary"
                  >
                    Start New Research
                  </button>
                </div>
                
                <ResultDisplay
                  result={state.currentResult}
                  onDownload={handleDownload}
                />
              </div>
            )}
          </>
        )}

        {/* Results Management View */}
        {state.currentView === 'results' && (
          <ResearchResultsList
            onViewResult={handleViewResult}
            onEditResult={handleEditResult}
          />
        )}

        {/* Result Editor Modal */}
        {state.selectedResult && (
          <ResearchResultEditor
            result={state.selectedResult}
            onClose={handleCloseResultEditor}
            onSave={handleResultSaved}
          />
        )}

        {/* Footer */}
        <footer className="mt-16 pt-8 border-t border-gray-200">
          <div className="text-center text-sm text-gray-500">
            <p>Cyber-Researcher v1.0.0 - Powered by Claude and STORM Framework</p>
            <p className="mt-1">
              A narrative-focused cybersecurity research assistant that blends historical context with technical analysis.
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;