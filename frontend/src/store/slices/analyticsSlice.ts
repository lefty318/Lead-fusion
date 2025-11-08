import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface DashboardData {
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

interface PerformanceData {
  agent_performance: Array<{
    agent: string;
    conversations_handled: number;
    avg_lead_score: number;
  }>;
}

interface AnalyticsState {
  dashboard: DashboardData | null;
  performance: PerformanceData | null;
  loading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  dashboard: null,
  performance: null,
  loading: false,
  error: null,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    fetchDashboardStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchDashboardSuccess: (state, action: PayloadAction<DashboardData>) => {
      state.dashboard = action.payload;
      state.loading = false;
    },
    fetchDashboardFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    fetchPerformanceStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchPerformanceSuccess: (state, action: PayloadAction<PerformanceData>) => {
      state.performance = action.payload;
      state.loading = false;
    },
    fetchPerformanceFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  fetchDashboardStart,
  fetchDashboardSuccess,
  fetchDashboardFailure,
  fetchPerformanceStart,
  fetchPerformanceSuccess,
  fetchPerformanceFailure,
  clearError,
} = analyticsSlice.actions;

export default analyticsSlice.reducer;