/**
 * API client for Cyber-Researcher backend.
 */

import axios from 'axios';
import type {
  ResearchRequest,
  StartResearchResponse,
  ResearchSession,
  ResearchResult,
  SystemStatus,
} from '../types/research';

const API_BASE_URL = 'http://localhost:8234/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const researchApi = {
  /**
   * Start a new research session.
   */
  startResearch: async (request: ResearchRequest): Promise<StartResearchResponse> => {
    const response = await apiClient.post<StartResearchResponse>('/research/start', request);
    return response.data;
  },

  /**
   * Get the status of a research session.
   */
  getResearchStatus: async (sessionId: string): Promise<ResearchSession> => {
    const response = await apiClient.get<ResearchSession>(`/research/${sessionId}/status`);
    return response.data;
  },

  /**
   * Get the result of a completed research session.
   */
  getResearchResult: async (sessionId: string): Promise<ResearchResult | null> => {
    const response = await apiClient.get<ResearchResult[]>(`/research/${sessionId}/result`);
    // The API returns an array of results, get the first one
    return response.data.length > 0 ? response.data[0] : null;
  },

  /**
   * List all research sessions.
   */
  listResearchSessions: async (): Promise<ResearchSession[]> => {
    const response = await apiClient.get<ResearchSession[]>('/research/sessions');
    return response.data;
  },

  /**
   * Delete a research session.
   */
  deleteResearchSession: async (sessionId: string): Promise<void> => {
    await apiClient.delete(`/research/${sessionId}`);
  },

  /**
   * Get system configuration and status.
   */
  getSystemConfig: async (): Promise<SystemStatus> => {
    const response = await apiClient.get<SystemStatus>('/config');
    return response.data;
  },
};

// Research Results Management API
export interface ResearchResultsListParams {
  page?: number;
  limit?: number;
  search?: string;
  output_format?: string;
  sort_by?: 'created_at' | 'title' | 'updated_at';
  sort_order?: 'asc' | 'desc';
}

export interface ResearchResultsListResponse {
  results: ResearchResult[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface UpdateResearchResultRequest {
  title?: string;
  content?: string;
  metadata?: Record<string, unknown>;
  tags?: string[];
  summary?: string;
}

export const researchResultsApi = {
  /**
   * List research results with pagination and filtering.
   */
  listResults: async (params: ResearchResultsListParams = {}): Promise<ResearchResultsListResponse> => {
    const queryParams = new URLSearchParams();
    
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.limit) queryParams.append('limit', params.limit.toString());
    if (params.search) queryParams.append('search', params.search);
    if (params.output_format) queryParams.append('output_format', params.output_format);
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.sort_order) queryParams.append('sort_order', params.sort_order);

    const response = await apiClient.get<ResearchResultsListResponse>(
      `/research/results?${queryParams.toString()}`
    );
    return response.data;
  },

  /**
   * Get a specific research result by ID.
   */
  getResult: async (resultId: string): Promise<ResearchResult> => {
    const response = await apiClient.get<ResearchResult>(`/research/results/${resultId}`);
    return response.data;
  },

  /**
   * Update a research result.
   */
  updateResult: async (resultId: string, data: UpdateResearchResultRequest): Promise<ResearchResult> => {
    const response = await apiClient.put<ResearchResult>(`/research/results/${resultId}`, data);
    return response.data;
  },

  /**
   * Delete a research result.
   */
  deleteResult: async (resultId: string): Promise<void> => {
    await apiClient.delete(`/research/results/${resultId}`);
  },
};

export default apiClient;