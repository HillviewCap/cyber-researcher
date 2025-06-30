/**
 * Research result editor component with markdown editing capabilities.
 */

import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { MarkdownEditor } from './MarkdownEditor';
import { MarkdownViewer } from './MarkdownViewer';
import { researchResultsApi, type UpdateResearchResultRequest } from '../services/api';
import type { ResearchResult } from '../types/research';
import { 
  XMarkIcon,
  CheckIcon,
  ArrowLeftIcon,
  TagIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';

interface ResearchResultEditorProps {
  result: ResearchResult;
  onClose: () => void;
  onSave?: (updatedResult: ResearchResult) => void;
}

export const ResearchResultEditor: React.FC<ResearchResultEditorProps> = ({
  result,
  onClose,
  onSave
}) => {
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [editedData, setEditedData] = useState({
    title: result.title,
    content: result.content,
    summary: result.summary || '',
    tags: result.tags || []
  });
  const [newTag, setNewTag] = useState('');

  const updateMutation = useMutation({
    mutationFn: (data: UpdateResearchResultRequest) => 
      researchResultsApi.updateResult(result.session_id, data),
    onSuccess: (updatedResult) => {
      queryClient.invalidateQueries({ queryKey: ['research-results'] });
      setIsEditing(false);
      if (onSave) {
        onSave(updatedResult);
      }
    },
    onError: (error) => {
      console.error('Failed to update result:', error);
      alert('Failed to update research result. Please try again.');
    }
  });

  const handleSave = () => {
    const updateData: UpdateResearchResultRequest = {
      title: editedData.title.trim(),
      content: editedData.content,
      summary: editedData.summary.trim() || undefined,
      tags: editedData.tags.filter(tag => tag.trim().length > 0)
    };

    updateMutation.mutate(updateData);
  };

  const handleCancel = () => {
    setEditedData({
      title: result.title,
      content: result.content,
      summary: result.summary || '',
      tags: result.tags || []
    });
    setIsEditing(false);
  };

  const handleAddTag = () => {
    if (newTag.trim() && !editedData.tags.includes(newTag.trim())) {
      setEditedData(prev => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()]
      }));
      setNewTag('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setEditedData(prev => ({
      ...prev,
      tags: prev.tags.filter((tag: string) => tag !== tagToRemove)
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const hasChanges = () => {
    return (
      editedData.title !== result.title ||
      editedData.content !== result.content ||
      editedData.summary !== (result.summary || '') ||
      JSON.stringify(editedData.tags.sort()) !== JSON.stringify((result.tags || []).sort())
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getWordCount = () => {
    return editedData.content.split(/\s+/).filter((word: string) => word.length > 0).length;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl max-h-screen overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg"
            >
              <ArrowLeftIcon className="h-5 w-5" />
            </button>
            <DocumentTextIcon className="h-6 w-6 text-cyber-600" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {isEditing ? 'Edit Research Result' : 'View Research Result'}
              </h2>
              <p className="text-sm text-gray-500">
                Created: {formatDate(result.created_at)} • Session: {result.session_id}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="btn-primary"
              >
                Edit Result
              </button>
            ) : (
              <>
                <button
                  onClick={handleCancel}
                  className="btn-secondary"
                  disabled={updateMutation.isPending}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  disabled={!hasChanges() || updateMutation.isPending}
                  className="btn-primary flex items-center space-x-2"
                >
                  <CheckIcon className="h-4 w-4" />
                  <span>{updateMutation.isPending ? 'Saving...' : 'Save Changes'}</span>
                </button>
              </>
            )}
            
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden flex flex-col">
          {isEditing ? (
            <div className="flex-1 flex flex-col space-y-4 p-6">
              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  value={editedData.title}
                  onChange={(e) => setEditedData(prev => ({ ...prev, title: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
                  placeholder="Enter title..."
                />
              </div>

              {/* Summary */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Summary (Optional)
                </label>
                <textarea
                  value={editedData.summary}
                  onChange={(e) => setEditedData(prev => ({ ...prev, summary: e.target.value }))}
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
                  placeholder="Enter a brief summary..."
                />
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags
                </label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {editedData.tags.map((tag: string, index: number) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-cyber-100 text-cyber-800"
                    >
                      {tag}
                      <button
                        onClick={() => handleRemoveTag(tag)}
                        className="ml-1 text-cyber-600 hover:text-cyber-400"
                      >
                        <XMarkIcon className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 relative">
                    <TagIcon className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      value={newTag}
                      onChange={(e) => setNewTag(e.target.value)}
                      onKeyPress={handleKeyPress}
                      className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
                      placeholder="Add tag..."
                    />
                  </div>
                  <button
                    onClick={handleAddTag}
                    disabled={!newTag.trim()}
                    className="btn-secondary-sm"
                  >
                    Add
                  </button>
                </div>
              </div>

              {/* Content Editor */}
              <div className="flex-1 min-h-0">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Content ({getWordCount().toLocaleString()} words)
                </label>
                <MarkdownEditor
                  content={editedData.content}
                  onChange={(content) => setEditedData(prev => ({ ...prev, content }))}
                  placeholder="Enter your research content here..."
                  className="h-full"
                />
              </div>
            </div>
          ) : (
            <div className="flex-1 overflow-auto p-6 space-y-4">
              {/* Title */}
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{result.title}</h3>
                <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                  <span>{getWordCount().toLocaleString()} words</span>
                  <span>•</span>
                  <span className="capitalize">{result.output_format.replace('_', ' ')}</span>
                </div>
              </div>

              {/* Summary */}
              {result.summary && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-gray-900 mb-1">Summary</h4>
                  <p className="text-sm text-gray-700">{result.summary}</p>
                </div>
              )}

              {/* Tags */}
              {result.tags && result.tags.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Tags</h4>
                  <div className="flex flex-wrap gap-2">
                    {result.tags.map((tag: string, index: number) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-cyber-100 text-cyber-800"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Content */}
              <div className="border-t pt-4">
                <div className="max-h-96 overflow-auto">
                  <MarkdownViewer content={result.content} />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};