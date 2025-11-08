import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { fetchDashboardStart, fetchDashboardSuccess, fetchDashboardFailure, fetchPerformanceStart, fetchPerformanceSuccess, fetchPerformanceFailure } from '../../store/slices/analyticsSlice';
import { analyticsAPI } from '../../services/api';

const Analytics: React.FC = () => {
  const dispatch = useAppDispatch();
  const { dashboard, performance, loading } = useAppSelector((state) => state.analytics);
  const [selectedPeriod, setSelectedPeriod] = useState(30);

  useEffect(() => {
    loadAnalytics();
  }, [selectedPeriod]);

  const loadAnalytics = async () => {
    try {
      dispatch(fetchDashboardStart());
      const dashboardResponse = await analyticsAPI.getDashboard(selectedPeriod);
      dispatch(fetchDashboardSuccess(dashboardResponse.data));

      dispatch(fetchPerformanceStart());
      const performanceResponse = await analyticsAPI.getPerformance();
      dispatch(fetchPerformanceSuccess(performanceResponse.data));
    } catch (error: any) {
      dispatch(fetchDashboardFailure(error.message));
      dispatch(fetchPerformanceFailure(error.message));
    }
  };

  const handleExport = async (format: string) => {
    try {
      const response = await analyticsAPI.exportData(format, selectedPeriod);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `analytics_${selectedPeriod}days.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics & Reports</h1>
        <div className="flex items-center space-x-4">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
          <div className="flex space-x-2">
            <button
              onClick={() => handleExport('csv')}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Export CSV
            </button>
            <button
              onClick={() => handleExport('xlsx')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Export Excel
            </button>
            <button
              onClick={() => handleExport('pdf')}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            >
              Export PDF
            </button>
          </div>
        </div>
      </div>

      {dashboard && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500">Total Conversations</h3>
              <p className="text-3xl font-bold text-gray-900">{dashboard.total_conversations}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500">Total Leads</h3>
              <p className="text-3xl font-bold text-gray-900">{dashboard.total_leads}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500">Conversion Rate</h3>
              <p className="text-3xl font-bold text-gray-900">
                {dashboard.total_leads > 0 ? ((dashboard.conversion_funnel.converted / dashboard.total_leads) * 100).toFixed(1) : 0}%
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500">Avg Response Time</h3>
              <p className="text-3xl font-bold text-gray-900">{dashboard.avg_response_time_hours.toFixed(1)}h</p>
            </div>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Channel Distribution */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Conversations by Channel</h3>
              <div className="space-y-3">
                {Object.entries(dashboard.conversations_by_channel).map(([channel, count]) => (
                  <div key={channel} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">{channel}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{
                            width: `${(count / dashboard.total_conversations) * 100}%`
                          }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-500">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Status Distribution */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Conversations by Status</h3>
              <div className="space-y-3">
                {Object.entries(dashboard.conversations_by_status).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">{status}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-600 h-2 rounded-full"
                          style={{
                            width: `${(count / dashboard.total_conversations) * 100}%`
                          }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-500">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Conversion Funnel */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Conversion Funnel</h3>
            <div className="space-y-4">
              {[
                { label: 'Conversations', value: dashboard.conversion_funnel.conversations, color: 'bg-blue-500' },
                { label: 'Leads', value: dashboard.conversion_funnel.leads, color: 'bg-green-500' },
                { label: 'Qualified Leads', value: dashboard.conversion_funnel.qualified_leads, color: 'bg-yellow-500' },
                { label: 'Converted', value: dashboard.conversion_funnel.converted, color: 'bg-purple-500' },
              ].map((step, index) => (
                <div key={step.label} className="flex items-center space-x-4">
                  <div className="w-32 text-sm font-medium text-gray-700">{step.label}</div>
                  <div className="flex-1">
                    <div className="w-full bg-gray-200 rounded-full h-6">
                      <div
                        className={`${step.color} h-6 rounded-full flex items-center justify-end pr-2`}
                        style={{
                          width: `${(step.value / dashboard.conversion_funnel.conversations) * 100}%`
                        }}
                      >
                        <span className="text-xs font-medium text-white">{step.value}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Agent Performance */}
      {performance && performance.agent_performance.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Agent Performance</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Agent
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Conversations Handled
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Lead Score
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {performance.agent_performance.map((agent, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {agent.agent}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {agent.conversations_handled}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {agent.avg_lead_score.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;