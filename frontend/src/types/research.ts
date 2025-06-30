/**
 * TypeScript types for research API.
 */

export const OutputFormat = {
  BLOG_POST: 'blog_post',
  BOOK_CHAPTER: 'book_chapter',
  RESEARCH_REPORT: 'research_report',
  INTERACTIVE_SESSION: 'interactive_session',
} as const;
export type OutputFormat = typeof OutputFormat[keyof typeof OutputFormat];

export const TechnicalDepth = {
  BEGINNER: 'beginner',
  INTERMEDIATE: 'intermediate',
  ADVANCED: 'advanced',
  EXPERT: 'expert',
} as const;
export type TechnicalDepth = typeof TechnicalDepth[keyof typeof TechnicalDepth];

export const TargetAudience = {
  GENERAL_PUBLIC: 'general_public',
  CYBERSECURITY_PROFESSIONALS: 'cybersecurity_professionals',
  STUDENTS: 'students',
  EXECUTIVES: 'executives',
  TECHNICAL_TEAMS: 'technical_teams',
} as const;
export type TargetAudience = typeof TargetAudience[keyof typeof TargetAudience];

export const ResearchStatus = {
  PENDING: 'pending',
  INITIALIZING: 'initializing',
  RESEARCHING: 'researching',
  ANALYZING: 'analyzing',
  GENERATING: 'generating',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const;
export type ResearchStatus = typeof ResearchStatus[keyof typeof ResearchStatus];

export interface ResearchRequest {
  topic: string;
  content_directions: string;
  output_format: OutputFormat;
  target_audience: TargetAudience;
  technical_depth: TechnicalDepth;
  include_historical_context: boolean;
  style: string;
  chapter_number?: number;
  learning_objectives?: string[];
  report_type?: string;
  confidentiality?: string;
}

export interface ProgressUpdate {
  session_id: string;
  status: ResearchStatus;
  progress_percentage: number;
  current_step: string;
  estimated_completion?: string;
  agent_activity: Record<string, string>;
}

export interface ResearchResult {
  session_id: string;
  title: string;
  content: string;
  metadata: Record<string, any>;
  sources: string[];
  agent_contributions: Record<string, Record<string, any>>;
  created_at: string;
  output_format: OutputFormat;
  summary?: string;
  tags?: string[];
  key_concepts?: string[];
  exercises?: string[];
  learning_objectives?: string[];
}

export interface ResearchSession {
  session_id: string;
  request: ResearchRequest;
  status: ResearchStatus;
  created_at: string;
  updated_at: string;
  progress_percentage: number;
  current_step: string;
  result?: ResearchResult;
  error_message?: string;
}

export interface StartResearchResponse {
  session_id: string;
  status: ResearchStatus;
  message: string;
}

export interface SystemStatus {
  agents: Record<string, string>;
  retrieval: Record<string, string>;
  configuration: Record<string, any>;
  output_directory: string;
}