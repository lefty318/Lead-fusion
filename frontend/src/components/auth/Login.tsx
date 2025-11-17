import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { loginStart, loginSuccess, loginFailure } from '../../store/slices/authSlice';
import { authAPI } from '../../services/api';
import { socketService } from '../../services/socket';

console.log('Login component loaded');

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { loading, error } = useAppSelector((state) => state.auth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Login attempt started for email:', email);
    dispatch(loginStart());

    try {
      console.log('Making login API call...');
      const response = await authAPI.login(email, password);
      console.log('Login API response:', response);
      const { access_token } = response.data;
      console.log('Access token received:', access_token ? 'Yes' : 'No');
      console.log('Token value:', access_token);

      localStorage.setItem('token', access_token);
      console.log('Token saved to localStorage:', localStorage.getItem('token'));

      // Fetch user info after login
      console.log('Fetching user info...');
      const userResponse = await authAPI.getCurrentUser();
      console.log('User info response:', userResponse);
      const user = userResponse.data;
      console.log('User data:', user);

      dispatch(loginSuccess({ user, token: access_token }));

      // Connect to socket
      console.log('Connecting to socket...');
      socketService.connect(access_token);

      // Redirect to dashboard
      console.log('Redirecting to dashboard...');
      navigate('/');
    } catch (error: any) {
      console.error('Login failed:', error);
      console.error('Error response:', error.response);
      console.error('Error data:', error.response?.data);
      
      let errorMessage = 'Login failed';
      
      if (!error.response) {
        // Network error - backend not reachable
        errorMessage = 'Cannot connect to server. Please ensure the backend server is running on http://localhost:8000';
      } else if (error.response.status === 401) {
        // Unauthorized - wrong credentials
        errorMessage = error.response?.data?.detail || 'Incorrect email or password';
      } else if (error.response.status === 422) {
        // Validation error
        errorMessage = error.response?.data?.detail || 'Please provide valid email and password';
      } else if (error.response.status === 500) {
        // Server error
        errorMessage = 'Server error. Please try again later or contact support.';
      } else {
        // Other errors
        errorMessage = error.response?.data?.detail || errorMessage;
      }
      
      dispatch(loginFailure(errorMessage));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to Lead Fusion
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <button
              type="button"
              onClick={() => navigate('/register')}
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              create a new account
            </button>
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <div className="text-red-600 text-sm text-center">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;