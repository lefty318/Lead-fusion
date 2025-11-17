import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { Provider } from 'react-redux';
import { store } from './store';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import Conversations from './components/conversations/Conversations';
import Analytics from './components/analytics/Analytics';
import Layout from './components/layout/Layout';
import { useAppSelector } from './hooks/redux';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  console.log('PrivateRoute check - isAuthenticated:', isAuthenticated);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/conversations"
              element={
                <PrivateRoute>
                  <Layout>
                    <Conversations />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/analytics"
              element={
                <PrivateRoute>
                  <Layout>
                    <Analytics />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
