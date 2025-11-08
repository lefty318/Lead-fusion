import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { conversationsAPI } from '../../services/api';
import { addMessage } from '../../store/slices/conversationsSlice';
import { Message } from '../../types/api';

interface ConversationDetailProps {
  conversationId: number;
}

const ConversationDetail: React.FC<ConversationDetailProps> = ({ conversationId }) => {
  const dispatch = useAppDispatch();
  const { currentConversation } = useAppSelector((state) => state.conversations);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadConversationDetails();
  }, [conversationId]);

  const loadConversationDetails = async () => {
    try {
      const [convResponse, messagesResponse] = await Promise.all([
        conversationsAPI.getConversation(conversationId),
        conversationsAPI.getMessages(conversationId),
      ]);

      setMessages(messagesResponse.data);
    } catch (error) {
      console.error('Error loading conversation details:', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setLoading(true);
    try {
      await conversationsAPI.sendReply(conversationId, newMessage);

      // Add message to local state
      const messageData: Message = {
        id: Date.now(), // Temporary ID until server responds
        conversation_id: conversationId,
        direction: 'outbound',
        content: newMessage,
        sent_at: new Date().toISOString(),
      };
      dispatch(addMessage({ conversationId, message: messageData }));
      setMessages(prev => [...prev, messageData]);
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEscalate = async () => {
    // Implementation for escalation would go here
    console.log('Escalate conversation:', conversationId);
  };

  if (!currentConversation) {
    return <div className="p-8 text-center text-gray-500">Loading conversation...</div>;
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-lg">
              {currentConversation.channel === 'whatsapp' ? '📱' :
               currentConversation.channel === 'facebook' ? '👥' :
               currentConversation.channel === 'instagram' ? '📸' : '💬'}
            </span>
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                {currentConversation.sender_name}
              </h3>
              <p className="text-sm text-gray-500 capitalize">
                {currentConversation.channel} • {currentConversation.status}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {currentConversation.needs_human && (
              <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800">
                Needs Human Attention
              </span>
            )}
            <button
              onClick={handleEscalate}
              className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
            >
              Escalate
            </button>
          </div>
        </div>

        {/* AI Insights */}
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <h4 className="text-sm font-medium text-blue-900">AI Insights</h4>
          <div className="mt-2 grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-blue-700">Intent:</span>
              <span className="ml-2 text-blue-900 capitalize">{currentConversation.intent || 'Unknown'}</span>
            </div>
            <div>
              <span className="text-blue-700">Sentiment:</span>
              <span className={`ml-2 ${currentConversation.sentiment > 0 ? 'text-green-600' : currentConversation.sentiment < 0 ? 'text-red-600' : 'text-gray-600'}`}>
                {currentConversation.sentiment > 0 ? 'Positive' : currentConversation.sentiment < 0 ? 'Negative' : 'Neutral'}
              </span>
            </div>
            <div>
              <span className="text-blue-700">Lead Score:</span>
              <span className="ml-2 text-blue-900">{currentConversation.lead_score.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-blue-700">Confidence:</span>
              <span className="ml-2 text-blue-900">{(currentConversation.ai_confidence * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.direction === 'outbound' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.direction === 'outbound'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-900'
              }`}
            >
              <p className="text-sm">{message.content}</p>
              <p className={`text-xs mt-1 ${message.direction === 'outbound' ? 'text-indigo-200' : 'text-gray-500'}`}>
                {new Date(message.sent_at).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Message Input */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !newMessage.trim()}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ConversationDetail;