/**
 * API client for Cyber-Researcher backend.
 */

import axios from 'axios';
import {
  ResearchRequest,
  StartResearchResponse,
  ResearchSession,
  ResearchResult,
  SystemStatus,
} from '../types/research';

const API_BASE_URL = 'http://localhost:8000/api';

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
  getResearchResult: async (sessionId: string): Promise<ResearchResult> => {
    const response = await apiClient.get<ResearchResult>(`/research/${sessionId}/result`);
    return response.data;
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

export default apiClient;