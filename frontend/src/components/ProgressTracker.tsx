/**
 * Progress tracker component for research sessions.
 */

import React from 'react';
import { ResearchStatus, ProgressUpdate } from '../types/research';

interface ProgressTrackerProps {
  update: ProgressUpdate | null;
  isConnected: boolean;
  error?: string | null;
}

const statusMessages = {
  [ResearchStatus.PENDING]: 'Preparing research session...',
  [ResearchStatus.INITIALIZING]: 'Initializing agents and retrieval systems...',
  [ResearchStatus.RESEARCHING]: 'Conducting research and analysis...',
  [ResearchStatus.ANALYZING]: 'Analyzing findings and synthesizing insights...',
  [ResearchStatus.GENERATING]: 'Generating final content...',
  [ResearchStatus.COMPLETED]: 'Research completed successfully!',
  [ResearchStatus.FAILED]: 'Research failed. Please try again.',
};

const statusColors = {
  [ResearchStatus.PENDING]: 'text-yellow-600',
  [ResearchStatus.INITIALIZING]: 'text-blue-600',
  [ResearchStatus.RESEARCHING]: 'text-cyan-600',
  [ResearchStatus.ANALYZING]: 'text-purple-600',
  [ResearchStatus.GENERATING]: 'text-indigo-600',
  [ResearchStatus.COMPLETED]: 'text-green-600',
  [ResearchStatus.FAILED]: 'text-red-600',
};

const progressColors = {
  [ResearchStatus.PENDING]: 'bg-yellow-200',
  [ResearchStatus.INITIALIZING]: 'bg-blue-200',
  [ResearchStatus.RESEARCHING]: 'bg-cyan-200',
  [ResearchStatus.ANALYZING]: 'bg-purple-200',
  [ResearchStatus.GENERATING]: 'bg-indigo-200',
  [ResearchStatus.COMPLETED]: 'bg-green-200',
  [ResearchStatus.FAILED]: 'bg-red-200',
};

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ update, isConnected, error }) => {
  if (!update) {
    return (
      <div className="card">
        <div className="text-center text-gray-500">
          Waiting for research session to start...
        </div>
      </div>
    );
  }

  const { status, progress_percentage, current_step, agent_activity } = update;

  return (
    <div className="card">
      {/* Connection Status */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Research Progress</h3>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
          <span className="text-sm text-gray-600">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-sm text-red-600">Connection Error: {error}</div>
        </div>
      )}

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Progress</span>
          <span>{progress_percentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all duration-500 ${progressColors[status] || 'bg-gray-400'}`}
            style={{ width: `${progress_percentage}%` }}
          ></div>
        </div>
      </div>

      {/* Status */}
      <div className="mb-4">
        <div className={`text-lg font-medium mb-1 ${statusColors[status] || 'text-gray-600'}`}>
          {statusMessages[status] || 'Processing...'}
        </div>
        <div className="text-sm text-gray-600">{current_step}</div>
      </div>

      {/* Agent Activity */}
      {Object.keys(agent_activity || {}).length > 0 && (
        <div className="border-t pt-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Agent Activity</h4>
          <div className="space-y-2">
            {Object.entries(agent_activity).map(([agent, activity]) => (
              <div key={agent} className="flex justify-between text-sm">
                <span className="text-gray-600 capitalize">
                  {agent.replace('_', ' ')}:
                </span>
                <span className="text-gray-900">{activity}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Research Steps Indicator */}
      <div className="border-t pt-4 mt-4">
        <div className="flex justify-between text-xs text-gray-500">
          <div className={`flex flex-col items-center ${
            [ResearchStatus.INITIALIZING, ResearchStatus.RESEARCHING, ResearchStatus.ANALYZING, 
             ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status) 
              ? 'text-cyber-600' : ''
          }`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${
              [ResearchStatus.INITIALIZING, ResearchStatus.RESEARCHING, ResearchStatus.ANALYZING,
               ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status)
                ? 'bg-cyber-600' : 'bg-gray-300'
            }`}></div>
            <span>Init</span>
          </div>
          
          <div className={`flex flex-col items-center ${
            [ResearchStatus.RESEARCHING, ResearchStatus.ANALYZING, ResearchStatus.GENERATING, 
             ResearchStatus.COMPLETED].includes(status) 
              ? 'text-cyber-600' : ''
          }`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${
              [ResearchStatus.RESEARCHING, ResearchStatus.ANALYZING, ResearchStatus.GENERATING,
               ResearchStatus.COMPLETED].includes(status)
                ? 'bg-cyber-600' : 'bg-gray-300'
            }`}></div>
            <span>Research</span>
          </div>
          
          <div className={`flex flex-col items-center ${
            [ResearchStatus.ANALYZING, ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status)
              ? 'text-cyber-600' : ''
          }`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${
              [ResearchStatus.ANALYZING, ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status)
                ? 'bg-cyber-600' : 'bg-gray-300'
            }`}></div>
            <span>Analyze</span>
          </div>
          
          <div className={`flex flex-col items-center ${
            [ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status)
              ? 'text-cyber-600' : ''
          }`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${
              [ResearchStatus.GENERATING, ResearchStatus.COMPLETED].includes(status)
                ? 'bg-cyber-600' : 'bg-gray-300'
            }`}></div>
            <span>Generate</span>
          </div>
          
          <div className={`flex flex-col items-center ${
            status === ResearchStatus.COMPLETED ? 'text-green-600' : ''
          }`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${
              status === ResearchStatus.COMPLETED ? 'bg-green-600' : 'bg-gray-300'
            }`}></div>
            <span>Complete</span>
          </div>
        </div>
      </div>
    </div>
  );
};