/**
 * Result display component for completed research.
 */

import React, { useState } from 'react';
import { OutputFormat } from '../types/research';
import type { ResearchResult, AgentActivity, AgentContribution } from '../types/research';
import { MarkdownViewer } from './MarkdownViewer';
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

  // Guard clause for incomplete or missing result
  if (!result || !result.content) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <p className="text-gray-500">No content available yet...</p>
        </div>
      </div>
    );
  }

  const FormatIcon = formatIcons[result.output_format] || DocumentTextIcon;

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
    if (!result?.content) return 0;
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
            <div className="text-sm text-gray-700 prose prose-sm max-w-none">
              <MarkdownViewer content={result.summary} className="text-sm" />
            </div>
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
        <div className="max-h-96 overflow-auto">
          <MarkdownViewer content={result.content} />
        </div>
      )}

      {activeTab === 'metadata' && (
        <div className="space-y-6">
          {/* Agent Workflow Section */}
          {result.workflow_metadata && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <span className="w-2 h-2 bg-cyber-500 rounded-full mr-2"></span>
                Agent Workflow Process
              </h3>
              
              {/* Workflow Summary */}
              {result.workflow_metadata?.workflow_summary && (
                <div className="bg-gradient-to-r from-cyber-50 to-blue-50 rounded-lg p-4 mb-4">
                  <h4 className="font-medium text-gray-900 mb-2">Research Session Summary</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Agents Used:</span>
                      <div className="font-medium">
                        {result.workflow_metadata.workflow_summary.agents_used?.length || 0}
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Total Steps:</span>
                      <div className="font-medium">
                        {result.workflow_metadata.workflow_summary.total_steps || 0}
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Completed:</span>
                      <div className="font-medium text-green-600">
                        {result.workflow_metadata.workflow_summary.completed_steps || 0}
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Status:</span>
                      <div className={`font-medium ${
                        result.workflow_metadata.workflow_summary.status === 'completed' 
                          ? 'text-green-600' 
                          : 'text-yellow-600'
                      }`}>
                        {result.workflow_metadata.workflow_summary.status}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Agent Activities Timeline */}
              {result.workflow_metadata?.agent_activities && (
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h4 className="font-medium text-gray-900 mb-3">Agent Activities Timeline</h4>
                  <div className="space-y-3">
                    {result.workflow_metadata.agent_activities.map((activity: AgentActivity, index: number) => (
                      <div key={activity.activity_id || index} className="flex items-start space-x-3 p-3 bg-white rounded border">
                        <div className={`w-3 h-3 rounded-full mt-1 ${
                          activity.status === 'completed' ? 'bg-green-500' :
                          activity.status === 'failed' ? 'bg-red-500' : 'bg-yellow-500'
                        }`}></div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <h5 className="font-medium text-gray-900 capitalize">
                              {activity.agent_name?.replace('_', ' ')} - {activity.step_name}
                            </h5>
                            <span className="text-xs text-gray-500">
                              Step {activity.step_order}
                            </span>
                          </div>
                          <div className="text-sm text-gray-600 mt-1">
                            Status: <span className={`font-medium ${
                              activity.status === 'completed' ? 'text-green-600' :
                              activity.status === 'failed' ? 'text-red-600' : 'text-yellow-600'
                            }`}>{activity.status}</span>
                            {activity.duration_seconds && (
                              <span className="ml-3">
                                Duration: {activity.duration_seconds}s
                              </span>
                            )}
                          </div>
                          {activity.error_message && (
                            <div className="text-sm text-red-600 mt-1">
                              Error: {activity.error_message}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Generation Process */}
          {result.generation_process && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                Generation Process
              </h3>
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="grid grid-cols-3 gap-4 text-sm mb-3">
                  <div>
                    <span className="text-gray-600">Total Steps:</span>
                    <div className="font-medium">{result.generation_process.total_steps}</div>
                  </div>
                  <div>
                    <span className="text-gray-600">Completed:</span>
                    <div className="font-medium text-green-600">{result.generation_process.completed_steps}</div>
                  </div>
                  <div>
                    <span className="text-gray-600">Failed:</span>
                    <div className="font-medium text-red-600">{result.generation_process.failed_steps}</div>
                  </div>
                </div>
                {result.generation_process.steps && (
                  <div className="space-y-2">
                    {result.generation_process.steps.map((step, index: number) => (
                      <div key={index} className="flex items-center justify-between text-sm">
                        <span className="font-medium">{step.agent} - {step.action}</span>
                        <div className="flex items-center space-x-2">
                          {step.duration_seconds && (
                            <span className="text-gray-500">{step.duration_seconds}s</span>
                          )}
                          <span className={`px-2 py-1 rounded text-xs ${
                            step.status === 'completed' ? 'bg-green-100 text-green-800' :
                            step.status === 'failed' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {step.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Agent Contributions Summary */}
          {result.agent_workflow_summary && Object.keys(result.agent_workflow_summary).length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                Agent Contributions Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(result.agent_workflow_summary).map(([agent, contribution]: [string, AgentContribution]) => (
                  <div key={agent} className="bg-purple-50 rounded-lg p-4">
                    <h4 className="font-medium text-purple-900 capitalize mb-2">
                      {agent.replace('_', ' ')}
                    </h4>
                    <div className="text-sm space-y-1">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Status:</span>
                        <span className={`font-medium ${
                          contribution.status === 'completed' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {contribution.status}
                        </span>
                      </div>
                      {contribution.steps_completed && (
                        <div className="flex justify-between">
                          <span className="text-gray-600">Steps:</span>
                          <span className="font-medium">{contribution.steps_completed}</span>
                        </div>
                      )}
                      {contribution.total_duration && (
                        <div className="flex justify-between">
                          <span className="text-gray-600">Duration:</span>
                          <span className="font-medium">{contribution.total_duration}s</span>
                        </div>
                      )}
                      {contribution.sources && contribution.sources.length > 0 && (
                        <div>
                          <span className="text-gray-600">Sources:</span>
                          <div className="font-medium">{contribution.sources.length} sources</div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Content Format Specific Fields */}
          {(result.learning_objectives || result.key_concepts || result.exercises) && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Content Metadata
              </h3>
              <div className="space-y-4">
                {result.learning_objectives && result.learning_objectives.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Learning Objectives</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-700 bg-green-50 rounded-lg p-3">
                      {result.learning_objectives.map((objective, index) => (
                        <li key={index}>{objective}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.key_concepts && result.key_concepts.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Key Concepts</h4>
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
                    <h4 className="font-medium text-gray-900 mb-2">Exercises</h4>
                    <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700 bg-blue-50 rounded-lg p-3">
                      {result.exercises.map((exercise, index) => (
                        <li key={index}>{exercise}</li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Technical Metadata */}
          {result.metadata && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <span className="w-2 h-2 bg-gray-500 rounded-full mr-2"></span>
                Technical Metadata
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-xs overflow-auto text-gray-700">
                  {JSON.stringify(result.metadata, null, 2)}
                </pre>
              </div>
            </div>
          )}
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