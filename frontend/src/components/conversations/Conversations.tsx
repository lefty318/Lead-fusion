import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { fetchConversationsStart, fetchConversationsSuccess, fetchConversationsFailure, setCurrentConversation } from '../../store/slices/conversationsSlice';
import { conversationsAPI } from '../../services/api';
import ConversationDetail from './ConversationDetail';
import { Conversation } from '../../types/api';

const Conversations: React.FC = () => {
  const dispatch = useAppDispatch();
  const { conversations, currentConversation, loading, filters } = useAppSelector((state) => state.conversations);
  const [selectedConversation, setSelectedConversation] = useState<number | null>(null);

  useEffect(() => {
    loadConversations();
  }, [filters]);

  const loadConversations = async () => {
    try {
      console.log('Loading conversations with filters:', filters);
      dispatch(fetchConversationsStart());
      const response = await conversationsAPI.getConversations({
        channel: filters.channel || undefined,
        status: filters.status || undefined,
      });
      console.log('Conversations loaded:', response.data);
      dispatch(fetchConversationsSuccess(response.data));
    } catch (error: any) {
      console.error('Conversations load failed:', error);
      dispatch(fetchConversationsFailure(error.message));
    }
  };

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

  const handleConversationClick = async (conversation: Conversation) => {
    setSelectedConversation(conversation.id);
    dispatch(setCurrentConversation(conversation));
  };

  return (
    <div className="flex h-screen">
      {/* Conversations List */}
      <div className="w-1/3 bg-white border-r border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Conversations</h2>
          <div className="mt-2 flex space-x-2">
            <select
              value={filters.channel || ''}
              onChange={(e) => dispatch({ type: 'conversations/setFilters', payload: { channel: e.target.value || null } })}
              className="text-sm border border-gray-300 rounded px-2 py-1"
            >
              <option value="">All Channels</option>
              <option value="whatsapp">WhatsApp</option>
              <option value="facebook">Facebook</option>
              <option value="instagram">Instagram</option>
            </select>
            <select
              value={filters.status || ''}
              onChange={(e) => dispatch({ type: 'conversations/setFilters', payload: { status: e.target.value || null } })}
              className="text-sm border border-gray-300 rounded px-2 py-1"
            >
              <option value="">All Status</option>
              <option value="open">Open</option>
              <option value="assigned">Assigned</option>
              <option value="escalated">Escalated</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </div>

        <div className="overflow-y-auto h-full">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              onClick={() => handleConversationClick(conversation)}
              className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                selectedConversation === conversation.id ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <span className="text-lg">{getChannelIcon(conversation.channel)}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {conversation.sender_name}
                    </p>
                    <p className="text-sm text-gray-500 truncate">
                      {conversation.message_text}
                    </p>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(conversation.status)}`}>
                        {conversation.status}
                      </span>
                      {conversation.needs_human && (
                        <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800">
                          Needs Human
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-xs text-gray-500">
                  {new Date(conversation.timestamp).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}

          {conversations.length === 0 && !loading && (
            <div className="p-8 text-center text-gray-500">
              No conversations found
            </div>
          )}

          {loading && (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
            </div>
          )}
        </div>
      </div>

      {/* Conversation Detail */}
      <div className="flex-1">
        {selectedConversation ? (
          <ConversationDetail conversationId={selectedConversation} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-500">
            Select a conversation to view details
          </div>
        )}
      </div>
    </div>
  );
};

export default Conversations;