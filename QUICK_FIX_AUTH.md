# Quick Fix: Authentication Errors

## Problem
You're seeing "Registration failed" or "Login failed" errors in the UI.

## Most Common Causes

### 1. Backend Server Not Running ⚠️ (MOST LIKELY)
The backend server must be running for authentication to work.

**Solution:**
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the server
python start_server.py
# OR
uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
```

**Verify it's running:**
- Open http://localhost:8000/health in your browser
- You should see: `{"status":"healthy"}`
- Or check API docs: http://localhost:8000/docs

### 2. Database Not Connected
The backend needs a database connection.

**Check database:**
```bash
cd backend
python -c "from app.database import engine; engine.connect(); print('Database connected!')"
```

**If using SQLite (default for development):**
- Check if `backend/leadfusion.db` exists
- If not, the database will be created automatically on first run

**If using PostgreSQL:**
- Ensure PostgreSQL is running
- Check `.env` file for `DATABASE_URL`
- Default: `postgresql://user:password@localhost/omnilead`

### 3. Frontend Not Connected to Backend
Check the API URL configuration.

**Verify:**
- Frontend expects backend at: `http://localhost:8000`
- Check `frontend/.env` for `REACT_APP_API_URL` (if set)
- Default in code: `http://localhost:8000`

### 4. CORS Issues
Backend CORS is configured for `http://localhost:3000` (React dev server).

**If using different port:**
- Edit `backend/app/main.py`
- Add your frontend URL to `allow_origins` in CORS middleware

## Quick Diagnostic Steps

1. **Check if backend is running:**
   ```bash
   # Windows PowerShell
   netstat -ano | findstr :8000
   
   # Should show a process listening on port 8000
   ```

2. **Test backend health:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

3. **Check browser console:**
   - Open Developer Tools (F12)
   - Check Console tab for detailed error messages
   - Check Network tab to see if requests are reaching the backend

4. **Check backend logs:**
   - Look at the terminal where backend is running
   - Check for database connection errors
   - Check for import errors

## Error Messages Explained

After the fix, you'll see more specific error messages:

- **"Cannot connect to server..."** → Backend not running
- **"Email already registered"** → User exists, try logging in instead
- **"Incorrect email or password"** → Wrong credentials
- **"Server error..."** → Backend issue, check backend logs
- **"Please fill in all required fields..."** → Validation error

## Complete Startup Sequence

1. **Start Backend:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   python start_server.py
   ```

2. **Start Frontend (in another terminal):**
   ```bash
   cd frontend
   npm start
   ```

3. **Verify:**
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## Still Having Issues?

1. Check backend terminal for error messages
2. Check browser console (F12) for detailed errors
3. Verify database connection
4. Ensure all dependencies are installed:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

