/**
 * Result display component for completed research.
 */

import React, { useState } from 'react';
import { OutputFormat } from '../types/research';
import type { ResearchResult } from '../types/research';
import { 
  DocumentArrowDownIcon, 
  ClipboardDocumentIcon,
  EyeIcon,
  DocumentTextIcon,
  BookOpenIcon,
  DocumentChartBarIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/react/24/outline';

interface ResultDisplayProps {
  result: ResearchResult;
  onDownload?: (format: 'markdown' | 'json' | 'txt') => void;
}

const formatIcons = {
  [OutputFormat.BLOG_POST]: DocumentTextIcon,
  [OutputFormat.BOOK_CHAPTER]: BookOpenIcon,
  [OutputFormat.RESEARCH_REPORT]: DocumentChartBarIcon,
  [OutputFormat.INTERACTIVE_SESSION]: ChatBubbleLeftRightIcon,
};

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onDownload }) => {
  const [activeTab, setActiveTab] = useState<'content' | 'metadata' | 'sources'>('content');
  const [copied, setCopied] = useState(false);

  const FormatIcon = formatIcons[result.output_format];

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getWordCount = () => {
    return result.content.split(/\s+/).length;
  };

  const getReadingTime = () => {
    const wordsPerMinute = 200;
    const minutes = Math.ceil(getWordCount() / wordsPerMinute);
    return minutes;
  };

  return (
    <div className="card">
      {/* Header */}
      <div className="border-b pb-4 mb-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <FormatIcon className="h-8 w-8 text-cyber-600" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{result.title}</h2>
              <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                <span>Created: {formatDate(result.created_at)}</span>
                <span>•</span>
                <span>{getWordCount().toLocaleString()} words</span>
                <span>•</span>
                <span>{getReadingTime()} min read</span>
              </div>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={handleCopyToClipboard}
              className="btn-secondary flex items-center space-x-2"
            >
              <ClipboardDocumentIcon className="h-4 w-4" />
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
            
            {onDownload && (
              <div className="relative group">
                <button className="btn-primary flex items-center space-x-2">
                  <DocumentArrowDownIcon className="h-4 w-4" />
                  <span>Download</span>
                </button>
                
                <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                  <button
                    onClick={() => onDownload('markdown')}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-t-lg"
                  >
                    Download as Markdown
                  </button>
                  <button
                    onClick={() => onDownload('txt')}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    Download as Text
                  </button>
                  <button
                    onClick={() => onDownload('json')}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-b-lg"
                  >
                    Download as JSON
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Summary and Tags */}
        {result.summary && (
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-1">Summary</h3>
            <p className="text-sm text-gray-700">{result.summary}</p>
          </div>
        )}
        
        {result.tags && result.tags.length > 0 && (
          <div className="mt-3">
            <div className="flex flex-wrap gap-2">
              {result.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyber-100 text-cyber-800"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="border-b mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('content')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'content'
                ? 'border-cyber-500 text-cyber-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <EyeIcon className="h-4 w-4 inline mr-2" />
            Content
          </button>
          <button
            onClick={() => setActiveTab('metadata')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'metadata'
                ? 'border-cyber-500 text-cyber-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Metadata
          </button>
          <button
            onClick={() => setActiveTab('sources')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'sources'
                ? 'border-cyber-500 text-cyber-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Sources ({result.sources.length})
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'content' && (
        <div className="prose prose-gray max-w-none">
          <div className="whitespace-pre-wrap font-mono text-sm bg-gray-50 rounded-lg p-4 overflow-auto max-h-96">
            {result.content}
          </div>
        </div>
      )}

      {activeTab === 'metadata' && (
        <div className="space-y-4">
          {/* Agent Contributions */}
          {Object.keys(result.agent_contributions).length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3">Agent Contributions</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(result.agent_contributions).map(([agent, contribution]) => (
                  <div key={agent} className="bg-gray-50 rounded-lg p-3">
                    <h4 className="font-medium text-gray-900 capitalize">
                      {agent.replace('_', ' ')}
                    </h4>
                    <div className="text-sm text-gray-600 mt-1">
                      {typeof contribution === 'object' && contribution !== null ? (
                        Object.entries(contribution).map(([key, value]) => (
                          <div key={key}>
                            <span className="capitalize">{key}:</span> {String(value)}
                          </div>
                        ))
                      ) : (
                        String(contribution)
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Additional Fields */}
          {result.learning_objectives && result.learning_objectives.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3">Learning Objectives</h3>
              <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                {result.learning_objectives.map((objective, index) => (
                  <li key={index}>{objective}</li>
                ))}
              </ul>
            </div>
          )}

          {result.key_concepts && result.key_concepts.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3">Key Concepts</h3>
              <div className="flex flex-wrap gap-2">
                {result.key_concepts.map((concept, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                  >
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {result.exercises && result.exercises.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3">Exercises</h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                {result.exercises.map((exercise, index) => (
                  <li key={index}>{exercise}</li>
                ))}
              </ol>
            </div>
          )}

          {/* Raw Metadata */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Technical Metadata</h3>
            <pre className="bg-gray-50 rounded-lg p-3 text-xs overflow-auto">
              {JSON.stringify(result.metadata, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {activeTab === 'sources' && (
        <div>
          {result.sources.length > 0 ? (
            <div className="space-y-2">
              {result.sources.map((source, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-700">
                    {source.startsWith('http') ? (
                      <a
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-cyber-600 hover:text-cyber-800 underline"
                      >
                        {source}
                      </a>
                    ) : (
                      source
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              No sources available for this research.
            </div>
          )}
        </div>
      )}
    </div>
  );
};