import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { fetchDashboardStart, fetchDashboardSuccess, fetchDashboardFailure } from '../../store/slices/analyticsSlice';
import { fetchConversationsStart, fetchConversationsSuccess, fetchConversationsFailure } from '../../store/slices/conversationsSlice';
import { analyticsAPI, conversationsAPI } from '../../services/api';

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { dashboard, loading: analyticsLoading } = useAppSelector((state) => state.analytics);
  const { conversations, loading: conversationsLoading } = useAppSelector((state) => state.conversations);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        dispatch(fetchDashboardStart());
        const response = await analyticsAPI.getDashboard();
        dispatch(fetchDashboardSuccess(response.data));
      } catch (error: any) {
        dispatch(fetchDashboardFailure(error.message));
      }
    };

    const loadRecentConversations = async () => {
      try {
        dispatch(fetchConversationsStart());
        const response = await conversationsAPI.getConversations({ limit: 5 });
        dispatch(fetchConversationsSuccess(response.data));
      } catch (error: any) {
        dispatch(fetchConversationsFailure(error.message));
      }
    };

    loadDashboard();
    loadRecentConversations();
  }, [dispatch]);

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case 'whatsapp': return '📱';
      case 'facebook': return '👥';
      case 'instagram': return '📸';
      default: return '💬';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-green-100 text-green-800';
      case 'escalated': return 'bg-red-100 text-red-800';
      case 'assigned': return 'bg-blue-100 text-blue-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to OmniLead - Your AI-powered conversation management platform</p>
      </div>

      {/* Stats Cards */}
      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <span className="text-2xl">💬</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Conversations</p>
                <p className="text-2xl font-bold text-gray-900">{dashboard.total_conversations}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Leads</p>
                <p className="text-2xl font-bold text-gray-900">{dashboard.total_leads}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <span className="text-2xl">⏱️</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-bold text-gray-900">{dashboard.avg_response_time_hours.toFixed(1)}h</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <span className="text-2xl">📈</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Conversion Rate</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboard.total_leads > 0 ? ((dashboard.conversion_funnel.converted / dashboard.total_leads) * 100).toFixed(1) : 0}%
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Conversations */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Conversations</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {conversations.slice(0, 5).map((conversation) => (
            <div key={conversation.id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <span className="text-lg mr-3">{getChannelIcon(conversation.channel)}</span>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{conversation.sender_name}</p>
                    <p className="text-sm text-gray-500 truncate max-w-md">{conversation.message_text}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(conversation.status)}`}>
                    {conversation.status}
                  </span>
                  <span className="text-sm text-gray-500">
                    {new Date(conversation.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
          {conversations.length === 0 && !conversationsLoading && (
            <div className="px-6 py-8 text-center text-gray-500">
              No conversations yet
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;