import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { Provider } from 'react-redux';
import { store } from './store';
import Login from './components/auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import Conversations from './components/conversations/Conversations';
import Analytics from './components/analytics/Analytics';
import Layout from './components/layout/Layout';
import { useAppSelector } from './hooks/redux';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/*"
              element={
                <PrivateRoute>
                  <Layout>
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/conversations" element={<Conversations />} />
                      <Route path="/analytics" element={<Analytics />} />
                      <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                  </Layout>
                </PrivateRoute>
              }
            />
          </Routes>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
