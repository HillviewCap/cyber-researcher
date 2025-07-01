/**
 * Research results list component with search, filtering, and pagination.
 */

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  researchResultsApi, 
  type ResearchResultsListParams,
  type ResearchResultsListResponse
} from '../services/api';
import type { ResearchResult } from '../types/research';
import { OutputFormat } from '../types/research';
import { MarkdownViewer } from './MarkdownViewer';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  DocumentTextIcon,
  BookOpenIcon,
  DocumentChartBarIcon,
  ChatBubbleLeftRightIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  CalendarIcon,
  TagIcon
} from '@heroicons/react/24/outline';

interface ResearchResultsListProps {
  onViewResult?: (result: ResearchResult) => void;
  onEditResult?: (result: ResearchResult) => void;
}

const formatIcons = {
  [OutputFormat.BLOG_POST]: DocumentTextIcon,
  [OutputFormat.BOOK_CHAPTER]: BookOpenIcon,
  [OutputFormat.RESEARCH_REPORT]: DocumentChartBarIcon,
  [OutputFormat.INTERACTIVE_SESSION]: ChatBubbleLeftRightIcon,
};

export const ResearchResultsList: React.FC<ResearchResultsListProps> = ({
  onViewResult,
  onEditResult
}) => {
  const queryClient = useQueryClient();
  const [params, setParams] = useState<ResearchResultsListParams>({
    page: 1,
    limit: 10,
    sort_by: 'created_at',
    sort_order: 'desc'
  });
  const [searchInput, setSearchInput] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Debounced search effect
  useEffect(() => {
    const timer = setTimeout(() => {
      setParams(prev => ({ ...prev, search: searchInput || undefined, page: 1 }));
    }, 500);

    return () => clearTimeout(timer);
  }, [searchInput]);

  const { data, isLoading, error } = useQuery<ResearchResultsListResponse>({
    queryKey: ['research-results', params],
    queryFn: () => researchResultsApi.listResults(params),
  });

  const deleteMutation = useMutation({
    mutationFn: (resultId: string) => researchResultsApi.deleteResult(resultId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['research-results'] });
    },
  });

  const handleDeleteResult = async (result: ResearchResult) => {
    if (window.confirm(`Are you sure you want to delete "${result.title}"?`)) {
      try {
        await deleteMutation.mutateAsync(result.session_id);
      } catch (error) {
        console.error('Failed to delete result:', error);
        alert('Failed to delete research result. Please try again.');
      }
    }
  };

  const handlePageChange = (newPage: number) => {
    setParams(prev => ({ ...prev, page: newPage }));
  };

  const handleSortChange = (sortBy: 'created_at' | 'title' | 'updated_at') => {
    setParams(prev => ({
      ...prev,
      sort_by: sortBy,
      sort_order: prev.sort_by === sortBy && prev.sort_order === 'desc' ? 'asc' : 'desc',
      page: 1
    }));
  };

  const handleFilterChange = (filterKey: string, value: string) => {
    setParams(prev => ({
      ...prev,
      [filterKey]: value || undefined,
      page: 1
    }));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getWordCount = (content: string) => {
    return content.split(/\s+/).filter(word => word.length > 0).length;
  };

  const truncateContent = (content: string, maxLength = 150) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  };

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-2">Failed to load research results</div>
        <button 
          onClick={() => queryClient.invalidateQueries({ queryKey: ['research-results'] })}
          className="btn-secondary"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Research Results</h2>
          <p className="text-gray-600">
            {data ? `${data.total} results found` : 'Loading...'}
          </p>
        </div>
        
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="btn-secondary flex items-center space-x-2"
        >
          <FunnelIcon className="h-4 w-4" />
          <span>Filters</span>
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search research results..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
        />
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Output Format
              </label>
              <select
                value={params.output_format || ''}
                onChange={(e) => handleFilterChange('output_format', e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
              >
                <option value="">All Formats</option>
                <option value={OutputFormat.BLOG_POST}>Blog Post</option>
                <option value={OutputFormat.BOOK_CHAPTER}>Book Chapter</option>
                <option value={OutputFormat.RESEARCH_REPORT}>Research Report</option>
                <option value={OutputFormat.INTERACTIVE_SESSION}>Interactive Session</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                value={params.sort_by || 'created_at'}
                onChange={(e) => handleSortChange(e.target.value as 'created_at' | 'title' | 'updated_at')}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
              >
                <option value="created_at">Created Date</option>
                <option value="title">Title</option>
                <option value="updated_at">Updated Date</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Results Per Page
              </label>
              <select
                value={params.limit || 10}
                onChange={(e) => handleFilterChange('limit', e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-cyber-500 focus:border-cyber-500"
              >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Results List */}
      {isLoading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            </div>
          ))}
        </div>
      ) : data && data.items && data.items.length > 0 ? (
        <div className="space-y-4">
          {data.items.map((result) => {
            const FormatIcon = formatIcons[result.output_format];
            
            return (
              <div key={result.session_id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <FormatIcon className="h-5 w-5 text-cyber-600" />
                      <h3 className="text-lg font-semibold text-gray-900">
                        {result.title}
                      </h3>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                      <div className="flex items-center space-x-1">
                        <CalendarIcon className="h-4 w-4" />
                        <span>{formatDate(result.created_at)}</span>
                      </div>
                      <span>•</span>
                      <span>{getWordCount(result.content).toLocaleString()} words</span>
                      <span>•</span>
                      <span className="capitalize">{result.output_format.replace('_', ' ')}</span>
                    </div>

                    {result.summary && (
                      <div className="text-gray-700 mb-3 prose prose-sm max-w-none">
                        <MarkdownViewer 
                          content={truncateContent(result.summary)} 
                          className="text-sm"
                        />
                      </div>
                    )}

                    {result.tags && result.tags.length > 0 && (
                      <div className="flex items-center space-x-2 mb-3">
                        <TagIcon className="h-4 w-4 text-gray-400" />
                        <div className="flex flex-wrap gap-1">
                          {result.tags.slice(0, 3).map((tag, index) => (
                            <span
                              key={index}
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-cyber-100 text-cyber-800"
                            >
                              {tag}
                            </span>
                          ))}
                          {result.tags.length > 3 && (
                            <span className="text-xs text-gray-500">
                              +{result.tags.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex items-center space-x-2 ml-4">
                    {onViewResult && (
                      <button
                        onClick={() => onViewResult(result)}
                        className="p-2 text-gray-400 hover:text-cyber-600 hover:bg-cyber-50 rounded-lg transition-colors"
                        title="View result"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </button>
                    )}
                    
                    {onEditResult && (
                      <button
                        onClick={() => onEditResult(result)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Edit result"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                    )}
                    
                    <button
                      onClick={() => handleDeleteResult(result)}
                      disabled={deleteMutation.isPending}
                      className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                      title="Delete result"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-12">
          <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
          <p className="text-gray-500">
            {searchInput ? 'Try adjusting your search terms or filters.' : 'Start by creating some research content.'}
          </p>
        </div>
      )}

      {/* Pagination */}
      {data && data.total > data.page_size && (
        <div className="flex items-center justify-between bg-white rounded-lg border border-gray-200 px-6 py-3">
          <div className="flex items-center space-x-2 text-sm text-gray-700">
            <span>
              Showing {((data.page - 1) * data.page_size) + 1} to {Math.min(data.page * data.page_size, data.total)} of {data.total} results
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(data.page - 1)}
              disabled={data.page <= 1}
              className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeftIcon className="h-4 w-4" />
            </button>
            
            <div className="flex space-x-1">
              {[...Array(Math.min(5, Math.ceil(data.total / data.page_size)))].map((_, i) => {
                const totalPages = Math.ceil(data.total / data.page_size);
                const pageNumber = Math.max(1, Math.min(totalPages - 4, data.page - 2)) + i;
                if (pageNumber > totalPages) return null;
                
                return (
                  <button
                    key={pageNumber}
                    onClick={() => handlePageChange(pageNumber)}
                    className={`px-3 py-1 text-sm rounded ${
                      pageNumber === data.page
                        ? 'bg-cyber-500 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {pageNumber}
                  </button>
                );
              })}
            </div>
            
            <button
              onClick={() => handlePageChange(data.page + 1)}
              disabled={data.page >= Math.ceil(data.total / data.page_size)}
              className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRightIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};