// API Response Types

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Conversation {
  id: number;
  external_id?: string;
  channel: string;
  sender_id: string;
  sender_name: string;
  recipient_id?: string;
  message_text: string;
  message_type?: string;
  timestamp: string;
  lead_score: number;
  sentiment: number;
  intent?: string;
  ai_confidence: number;
  needs_human: boolean;
  assigned_to?: number;
  status: string;
  created_at: string;
  updated_at?: string;
  messages?: Message[];
}

export interface Message {
  id: number;
  conversation_id: number;
  direction: 'inbound' | 'outbound';
  content: string;
  content_type?: string;
  sent_at: string;
  delivered_at?: string;
  read_at?: string;
}

export interface Lead {
  id: number;
  conversation_id: number;
  name?: string;
  phone?: string;
  email?: string;
  program_interest?: string;
  score: number;
  status: string;
  assigned_to?: number;
  created_at: string;
}

export interface AnalyticsDashboard {
  total_conversations: number;
  conversations_by_channel: Record<string, number>;
  conversations_by_status: Record<string, number>;
  total_leads: number;
  leads_by_status: Record<string, number>;
  avg_response_time_hours: number;
  conversion_funnel: {
    conversations: number;
    leads: number;
    qualified_leads: number;
    converted: number;
  };
}

export interface PerformanceMetrics {
  agent_performance: Array<{
    agent: string;
    conversations_handled: number;
    avg_lead_score: number;
  }>;
}

export interface AssignConversationRequest {
  user_id: number;
}

export interface ReplyRequest {
  content: string;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

// Request/Response types for API calls
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role: string;
}

export interface GetConversationsParams {
  skip?: number;
  limit?: number;
  channel?: string;
  status?: string;
}

export interface ExportDataParams {
  format: 'csv' | 'xlsx' | 'pdf';
  days?: number;
}

