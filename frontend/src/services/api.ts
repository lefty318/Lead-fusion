import axios, { AxiosResponse } from 'axios';
import {
  User,
  TokenResponse,
  Conversation,
  Message,
  AnalyticsDashboard,
  PerformanceMetrics,
  LoginRequest,
  RegisterRequest,
  GetConversationsParams,
  AssignConversationRequest,
  ReplyRequest,
} from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email: string, password: string): Promise<AxiosResponse<TokenResponse>> =>
    api.post<TokenResponse>('/api/auth/login', { username: email, password } as LoginRequest),
  register: (userData: RegisterRequest): Promise<AxiosResponse<TokenResponse>> =>
    api.post<TokenResponse>('/api/auth/register', userData),
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get<User>('/api/auth/me'),
};

export const conversationsAPI = {
  getConversations: (params?: GetConversationsParams): Promise<AxiosResponse<Conversation[]>> =>
    api.get<Conversation[]>('/api/conversations/', { params }),
  getConversation: (id: number): Promise<AxiosResponse<Conversation>> =>
    api.get<Conversation>(`/api/conversations/${id}`),
  getMessages: (id: number): Promise<AxiosResponse<Message[]>> =>
    api.get<Message[]>(`/api/conversations/${id}/messages`),
  assignConversation: (id: number, userId: number): Promise<AxiosResponse<{ message: string }>> =>
    api.post<{ message: string }>(`/api/conversations/${id}/assign`, { user_id: userId } as AssignConversationRequest),
  sendReply: (id: number, content: string): Promise<AxiosResponse<{ message: string }>> =>
    api.post<{ message: string }>(`/api/conversations/${id}/reply`, { content } as ReplyRequest),
};

export const analyticsAPI = {
  getDashboard: (days?: number): Promise<AxiosResponse<AnalyticsDashboard>> =>
    api.get<AnalyticsDashboard>('/api/analytics/dashboard', { params: { days } }),
  getPerformance: (): Promise<AxiosResponse<PerformanceMetrics>> =>
    api.get<PerformanceMetrics>('/api/analytics/performance'),
  exportData: (format: 'csv' | 'xlsx' | 'pdf', days?: number): Promise<AxiosResponse<Blob>> =>
    api.get<Blob>(`/api/analytics/export/${format}`, {
      params: { days },
      responseType: 'blob'
    }),
};

export default api;