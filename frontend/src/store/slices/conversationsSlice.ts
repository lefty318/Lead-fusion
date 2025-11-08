import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Conversation, Message } from '../../types/api';

interface ConversationsState {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  loading: boolean;
  error: string | null;
  filters: {
    channel: string | null;
    status: string | null;
  };
}

const initialState: ConversationsState = {
  conversations: [],
  currentConversation: null,
  loading: false,
  error: null,
  filters: {
    channel: null,
    status: null,
  },
};

const conversationsSlice = createSlice({
  name: 'conversations',
  initialState,
  reducers: {
    fetchConversationsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchConversationsSuccess: (state, action: PayloadAction<Conversation[]>) => {
      state.conversations = action.payload;
      state.loading = false;
    },
    fetchConversationsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    setCurrentConversation: (state, action: PayloadAction<Conversation>) => {
      state.currentConversation = action.payload;
    },
    updateConversation: (state, action: PayloadAction<Conversation>) => {
      const index = state.conversations.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.conversations[index] = action.payload;
      }
      if (state.currentConversation?.id === action.payload.id) {
        state.currentConversation = action.payload;
      }
    },
    addMessage: (state, action: PayloadAction<{ conversationId: number; message: Message }>) => {
      const conversation = state.conversations.find(c => c.id === action.payload.conversationId);
      if (conversation && conversation.messages) {
        conversation.messages.push(action.payload.message);
      }
      if (state.currentConversation?.id === action.payload.conversationId && state.currentConversation.messages) {
        state.currentConversation.messages.push(action.payload.message);
      }
    },
    setFilters: (state, action: PayloadAction<{ channel?: string | null; status?: string | null }>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  fetchConversationsStart,
  fetchConversationsSuccess,
  fetchConversationsFailure,
  setCurrentConversation,
  updateConversation,
  addMessage,
  setFilters,
  clearError,
} = conversationsSlice.actions;

export default conversationsSlice.reducer;