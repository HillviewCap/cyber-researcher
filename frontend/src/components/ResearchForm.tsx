/**
 * Research form component for starting new research sessions.
 */

import React, { useState } from 'react';
import { 
  OutputFormat, 
  TechnicalDepth, 
  TargetAudience
} from '../types/research';
import type { ResearchRequest } from '../types/research';

interface ResearchFormProps {
  onSubmit: (request: ResearchRequest) => void;
  isLoading?: boolean;
}

export const ResearchForm: React.FC<ResearchFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<ResearchRequest>({
    topic: '',
    content_directions: '',
    output_format: OutputFormat.BLOG_POST,
    target_audience: TargetAudience.CYBERSECURITY_PROFESSIONALS,
    technical_depth: TechnicalDepth.INTERMEDIATE,
    include_historical_context: true,
    style: 'educational',
    chapter_number: 1,
    learning_objectives: [],
    report_type: 'threat_assessment',
    confidentiality: 'internal',
  });

  const [learningObjectivesText, setLearningObjectivesText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Process learning objectives
    const objectives = learningObjectivesText
      .split('\n')
      .map(obj => obj.trim())
      .filter(obj => obj.length > 0);

    const request: ResearchRequest = {
      ...formData,
      learning_objectives: objectives.length > 0 ? objectives : undefined,
    };

    onSubmit(request);
  };

  const handleInputChange = (
    field: keyof ResearchRequest,
    value: string | number | boolean
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const isBookChapter = formData.output_format === OutputFormat.BOOK_CHAPTER;
  const isResearchReport = formData.output_format === OutputFormat.RESEARCH_REPORT;

  return (
    <div className="card max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Start New Research
        </h2>
        <p className="text-gray-600">
          Configure your cybersecurity research parameters and generate comprehensive content.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Topic */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            Research Topic *
          </label>
          <input
            type="text"
            id="topic"
            value={formData.topic}
            onChange={(e) => handleInputChange('topic', e.target.value)}
            placeholder="e.g., Ransomware Evolution and Defense Strategies"
            className="input-field"
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            The main topic or title for your research content.
          </p>
        </div>

        {/* Content Directions */}
        <div>
          <label htmlFor="content_directions" className="block text-sm font-medium text-gray-700 mb-2">
            Content Directions & Focus Areas *
          </label>
          <textarea
            id="content_directions"
            value={formData.content_directions}
            onChange={(e) => handleInputChange('content_directions', e.target.value)}
            placeholder="Describe specific insights, perspectives, or areas you want the research to explore. For example: Focus on the evolution from simple file encryption to sophisticated supply chain attacks, emphasize prevention strategies for small businesses, analyze historical parallels with pre-digital security threats."
            className="textarea-field"
            rows={4}
            required
          />
          <p className="mt-1 text-sm text-gray-500">
            Provide specific directions for what the content should explore and emphasize.
          </p>
        </div>

        {/* Output Format */}
        <div>
          <label htmlFor="output_format" className="block text-sm font-medium text-gray-700 mb-2">
            Output Format
          </label>
          <select
            id="output_format"
            value={formData.output_format}
            onChange={(e) => handleInputChange('output_format', e.target.value as OutputFormat)}
            className="input-field"
          >
            <option value={OutputFormat.BLOG_POST}>Blog Post</option>
            <option value={OutputFormat.BOOK_CHAPTER}>Book Chapter</option>
            <option value={OutputFormat.RESEARCH_REPORT}>Research Report</option>
            <option value={OutputFormat.INTERACTIVE_SESSION}>Interactive Session</option>
          </select>
        </div>

        {/* Configuration Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Target Audience */}
          <div>
            <label htmlFor="target_audience" className="block text-sm font-medium text-gray-700 mb-2">
              Target Audience
            </label>
            <select
              id="target_audience"
              value={formData.target_audience}
              onChange={(e) => handleInputChange('target_audience', e.target.value as TargetAudience)}
              className="input-field"
            >
              <option value={TargetAudience.CYBERSECURITY_PROFESSIONALS}>
                Cybersecurity Professionals
              </option>
              <option value={TargetAudience.STUDENTS}>Students</option>
              <option value={TargetAudience.EXECUTIVES}>Executives</option>
              <option value={TargetAudience.TECHNICAL_TEAMS}>Technical Teams</option>
              <option value={TargetAudience.GENERAL_PUBLIC}>General Public</option>
            </select>
          </div>

          {/* Technical Depth */}
          <div>
            <label htmlFor="technical_depth" className="block text-sm font-medium text-gray-700 mb-2">
              Technical Depth
            </label>
            <select
              id="technical_depth"
              value={formData.technical_depth}
              onChange={(e) => handleInputChange('technical_depth', e.target.value as TechnicalDepth)}
              className="input-field"
            >
              <option value={TechnicalDepth.BEGINNER}>Beginner</option>
              <option value={TechnicalDepth.INTERMEDIATE}>Intermediate</option>
              <option value={TechnicalDepth.ADVANCED}>Advanced</option>
              <option value={TechnicalDepth.EXPERT}>Expert</option>
            </select>
          </div>
        </div>

        {/* Style and Options */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="style" className="block text-sm font-medium text-gray-700 mb-2">
              Writing Style
            </label>
            <select
              id="style"
              value={formData.style}
              onChange={(e) => handleInputChange('style', e.target.value)}
              className="input-field"
            >
              <option value="educational">Educational</option>
              <option value="technical">Technical</option>
              <option value="narrative">Narrative</option>
            </select>
          </div>

          <div className="flex items-center pt-6">
            <input
              id="include_historical_context"
              type="checkbox"
              checked={formData.include_historical_context}
              onChange={(e) => handleInputChange('include_historical_context', e.target.checked)}
              className="h-4 w-4 text-cyber-600 focus:ring-cyber-500 border-gray-300 rounded"
            />
            <label htmlFor="include_historical_context" className="ml-2 block text-sm text-gray-900">
              Include Historical Context
            </label>
          </div>
        </div>

        {/* Book Chapter specific fields */}
        {isBookChapter && (
          <div className="border-t pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Book Chapter Options</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="chapter_number" className="block text-sm font-medium text-gray-700 mb-2">
                  Chapter Number
                </label>
                <input
                  type="number"
                  id="chapter_number"
                  value={formData.chapter_number || 1}
                  onChange={(e) => handleInputChange('chapter_number', parseInt(e.target.value))}
                  min="1"
                  className="input-field"
                />
              </div>
            </div>

            <div className="mt-4">
              <label htmlFor="learning_objectives" className="block text-sm font-medium text-gray-700 mb-2">
                Learning Objectives (one per line)
              </label>
              <textarea
                id="learning_objectives"
                value={learningObjectivesText}
                onChange={(e) => setLearningObjectivesText(e.target.value)}
                placeholder="Understand the historical evolution of cybersecurity threats&#10;Analyze modern attack vectors and defense strategies&#10;Apply security principles to real-world scenarios"
                className="textarea-field"
                rows={4}
              />
            </div>
          </div>
        )}

        {/* Research Report specific fields */}
        {isResearchReport && (
          <div className="border-t pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Research Report Options</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="report_type" className="block text-sm font-medium text-gray-700 mb-2">
                  Report Type
                </label>
                <select
                  id="report_type"
                  value={formData.report_type || 'threat_assessment'}
                  onChange={(e) => handleInputChange('report_type', e.target.value)}
                  className="input-field"
                >
                  <option value="threat_assessment">Threat Assessment</option>
                  <option value="incident_analysis">Incident Analysis</option>
                  <option value="vulnerability_analysis">Vulnerability Analysis</option>
                  <option value="risk_assessment">Risk Assessment</option>
                </select>
              </div>

              <div>
                <label htmlFor="confidentiality" className="block text-sm font-medium text-gray-700 mb-2">
                  Confidentiality Level
                </label>
                <select
                  id="confidentiality"
                  value={formData.confidentiality || 'internal'}
                  onChange={(e) => handleInputChange('confidentiality', e.target.value)}
                  className="input-field"
                >
                  <option value="public">Public</option>
                  <option value="internal">Internal</option>
                  <option value="confidential">Confidential</option>
                  <option value="restricted">Restricted</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end pt-6 border-t">
          <button
            type="submit"
            disabled={isLoading || !formData.topic || !formData.content_directions}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Starting Research...
              </>
            ) : (
              'Start Research'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};