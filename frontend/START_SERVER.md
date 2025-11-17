# How to Start the Frontend Server

## Quick Start

**Always run `npm start` from the `frontend` directory!**

### Option 1: Use the PowerShell Script (Recommended)
```powershell
# From project root or anywhere
.\frontend\start_frontend.ps1
```

### Option 2: Manual Start
```powershell
# Navigate to frontend directory first
cd frontend

# Then start the server
npm start
```

### Option 3: One-liner from Project Root
```powershell
cd frontend; npm start
```

## Common Error

If you see:
```
npm error Missing script: "start"
```

**Solution:** You're in the wrong directory. Make sure you're in the `frontend` folder before running `npm start`.

## Access the Application

Once the server starts (takes 30-60 seconds on first run):
- Main App: http://localhost:3000
- Registration: http://localhost:3000/#/register
- Login: http://localhost:3000/#/login

## Troubleshooting

1. **Port 3000 already in use?**
   - Stop any other React apps running on port 3000
   - Or set a different port: `$env:PORT = "3001"; npm start`

2. **Dependencies not installed?**
   - Run `npm install` in the `frontend` directory first

3. **Compilation errors?**
   - Make sure you're using React 18.3.1 (compatible with react-scripts 5.0.1)
   - Clear cache: `npm start -- --reset-cache`



