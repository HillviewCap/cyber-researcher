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

// Workflow metadata interfaces
export interface AgentActivity {
  activity_id: string;
  agent_name: string;
  step_name: string;
  step_order: number;
  status: string;
  start_time: string;
  end_time?: string;
  duration_seconds?: number;
  error_message?: string;
  retry_count: number;
  input_data?: Record<string, unknown>;
  output_data?: Record<string, unknown>;
}

export interface WorkflowSummary {
  agents_used: string[];
  total_steps: number;
  completed_steps: number;
  failed_steps: number;
  status: string;
  start_time: string;
  end_time?: string;
  total_duration_seconds?: number;
}

export interface GenerationStep {
  agent: string;
  action: string;
  status: string;
  start_time: string;
  end_time?: string;
  duration_seconds?: number;
}

export interface GenerationProcess {
  total_steps: number;
  completed_steps: number;
  failed_steps: number;
  steps: GenerationStep[];
  start_time: string;
  end_time?: string;
}

export interface AgentContribution {
  status: string;
  steps_completed: number;
  total_steps: number;
  total_duration: number;
  sources: string[];
  errors: string[];
}

export interface WorkflowMetadata {
  workflow_summary: WorkflowSummary;
  agent_activities: AgentActivity[];
}

export interface ResearchResult {
  session_id: string;
  title: string;
  content: string; // Final polished content only
  metadata: Record<string, unknown>; // Technical metadata only
  sources: string[];
  agent_contributions: Record<string, AgentContribution | Record<string, unknown>>; // Legacy compatibility
  created_at: string;
  output_format: OutputFormat;
  
  // Workflow separation fields
  workflow_metadata?: WorkflowMetadata; // Complete workflow information
  generation_process?: GenerationProcess; // Step-by-step process
  agent_workflow_summary?: Record<string, AgentContribution>; // Agent contributions summary
  
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
  configuration: Record<string, unknown>;
  output_directory: string;
}