/**
 * Markdown editor component with live preview and editing capabilities.
 */

import React, { useState, useRef, useEffect } from 'react';
import { MarkdownViewer } from './MarkdownViewer';
import { 
  EyeIcon, 
  PencilIcon, 
  DocumentDuplicateIcon,
  ArrowsPointingOutIcon,
  ArrowsPointingInIcon
} from '@heroicons/react/24/outline';

interface MarkdownEditorProps {
  content: string;
  onChange: (content: string) => void;
  onSave?: (content: string) => void;
  isLoading?: boolean;
  placeholder?: string;
  className?: string;
}

export const MarkdownEditor: React.FC<MarkdownEditorProps> = ({
  content,
  onChange,
  onSave,
  isLoading = false,
  placeholder = "Enter your content here...",
  className = ''
}) => {
  const [mode, setMode] = useState<'edit' | 'preview' | 'split'>('split');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isDirty, setIsDirty] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setIsDirty(false);
  }, [content]);

  const handleContentChange = (value: string) => {
    onChange(value);
    setIsDirty(true);
  };

  const handleSave = () => {
    if (onSave && isDirty) {
      onSave(content);
      setIsDirty(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Ctrl/Cmd + S to save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      handleSave();
    }
    
    // Tab for indentation
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newValue = content.substring(0, start) + '  ' + content.substring(end);
      
      handleContentChange(newValue);
      
      // Set cursor position after the inserted tab
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 2;
      });
    }
  };

  const insertText = (before: string, after: string = '') => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = content.substring(start, end);
    const newText = before + selectedText + after;
    const newValue = content.substring(0, start) + newText + content.substring(end);
    
    handleContentChange(newValue);
    
    // Set cursor position
    setTimeout(() => {
      const newCursorPos = start + before.length + (selectedText ? selectedText.length + after.length : 0);
      textarea.selectionStart = textarea.selectionEnd = newCursorPos;
      textarea.focus();
    });
  };

  const formatButtons = [
    { label: 'Bold', icon: 'B', action: () => insertText('**', '**') },
    { label: 'Italic', icon: 'I', action: () => insertText('*', '*') },
    { label: 'Code', icon: '`', action: () => insertText('`', '`') },
    { label: 'Link', icon: '🔗', action: () => insertText('[', '](url)') },
    { label: 'Header', icon: 'H', action: () => insertText('## ') },
    { label: 'List', icon: '•', action: () => insertText('- ') },
    { label: 'Quote', icon: '"', action: () => insertText('> ') },
    { label: 'Code Block', icon: '{', action: () => insertText('```\n', '\n```') },
  ];

  const containerClasses = `
    ${className} 
    ${isFullscreen ? 'fixed inset-0 z-50 bg-white' : 'relative'} 
    border border-gray-200 rounded-lg overflow-hidden
  `;

  return (
    <div className={containerClasses}>
      {/* Header */}
      <div className="flex items-center justify-between bg-gray-50 border-b border-gray-200 px-4 py-2">
        <div className="flex items-center space-x-2">
          {/* Mode Toggle */}
          <div className="flex bg-white border border-gray-200 rounded-lg">
            <button
              onClick={() => setMode('edit')}
              className={`px-3 py-1 text-xs font-medium rounded-l-lg ${
                mode === 'edit' 
                  ? 'bg-cyber-500 text-white' 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <PencilIcon className="h-3 w-3 inline mr-1" />
              Edit
            </button>
            <button
              onClick={() => setMode('split')}
              className={`px-3 py-1 text-xs font-medium ${
                mode === 'split' 
                  ? 'bg-cyber-500 text-white' 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <DocumentDuplicateIcon className="h-3 w-3 inline mr-1" />
              Split
            </button>
            <button
              onClick={() => setMode('preview')}
              className={`px-3 py-1 text-xs font-medium rounded-r-lg ${
                mode === 'preview' 
                  ? 'bg-cyber-500 text-white' 
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <EyeIcon className="h-3 w-3 inline mr-1" />
              Preview
            </button>
          </div>

          {/* Format Buttons */}
          {(mode === 'edit' || mode === 'split') && (
            <div className="flex space-x-1 border-l border-gray-300 pl-2">
              {formatButtons.map((btn, index) => (
                <button
                  key={index}
                  onClick={btn.action}
                  title={btn.label}
                  className="px-2 py-1 text-xs font-mono bg-white border border-gray-200 rounded hover:bg-gray-50"
                >
                  {btn.icon}
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2">
          {isDirty && (
            <span className="text-xs text-orange-600">Unsaved changes</span>
          )}
          
          {onSave && (
            <button
              onClick={handleSave}
              disabled={!isDirty || isLoading}
              className="btn-primary-sm"
            >
              {isLoading ? 'Saving...' : 'Save'}
            </button>
          )}

          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1 text-gray-400 hover:text-gray-600"
            title={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
          >
            {isFullscreen ? (
              <ArrowsPointingInIcon className="h-4 w-4" />
            ) : (
              <ArrowsPointingOutIcon className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className={`flex ${isFullscreen ? 'h-full' : 'h-96'}`}>
        {/* Editor Panel */}
        {(mode === 'edit' || mode === 'split') && (
          <div className={`${mode === 'split' ? 'w-1/2 border-r border-gray-200' : 'w-full'}`}>
            <textarea
              ref={textareaRef}
              value={content}
              onChange={(e) => handleContentChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              className="w-full h-full p-4 border-0 resize-none focus:outline-none focus:ring-0 font-mono text-sm"
              disabled={isLoading}
            />
          </div>
        )}

        {/* Preview Panel */}
        {(mode === 'preview' || mode === 'split') && (
          <div className={`${mode === 'split' ? 'w-1/2' : 'w-full'} overflow-auto`}>
            <div className="p-4">
              {content.trim() ? (
                <MarkdownViewer content={content} />
              ) : (
                <div className="text-gray-400 text-center py-8">
                  <EyeIcon className="h-12 w-12 mx-auto mb-2 opacity-50" />
                  <p>Preview will appear here...</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-50 border-t border-gray-200 px-4 py-2">
        <div className="flex justify-between items-center text-xs text-gray-500">
          <div className="flex space-x-4">
            <span>Words: {content.split(/\s+/).filter(word => word.length > 0).length}</span>
            <span>Characters: {content.length}</span>
            <span>Lines: {content.split('\n').length}</span>
          </div>
          <div>
            <span>Ctrl+S to save • Tab for indentation</span>
          </div>
        </div>
      </div>
    </div>
  );
};