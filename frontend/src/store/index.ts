import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import conversationsReducer from './slices/conversationsSlice';
import analyticsReducer from './slices/analyticsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    conversations: conversationsReducer,
    analytics: analyticsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;