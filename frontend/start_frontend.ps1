# Frontend Startup Script for Lead Fusion
Write-Host "🚀 Starting Lead Fusion Frontend..." -ForegroundColor Cyan
Write-Host "=" * 50

# Get the script directory and change to it if needed
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$currentDir = Get-Location

# If we're not in the frontend directory, change to it
if (-not (Test-Path "package.json")) {
    if (Test-Path (Join-Path $scriptDir "package.json")) {
        Write-Host "⚠️  Not in frontend directory. Changing to frontend directory..." -ForegroundColor Yellow
        Set-Location $scriptDir
        Write-Host "✅ Changed to: $(Get-Location)" -ForegroundColor Green
    } else {
        Write-Host "❌ Error: package.json not found. Make sure you're in the frontend directory." -ForegroundColor Red
        Write-Host "   Current directory: $currentDir" -ForegroundColor Red
        Write-Host "   Script directory: $scriptDir" -ForegroundColor Red
        exit 1
    }
}

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  node_modules not found. Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Check if port 3000 is available
$portCheck = netstat -ano | findstr ":3000"
if ($portCheck) {
    Write-Host "⚠️  Port 3000 is already in use!" -ForegroundColor Yellow
    Write-Host "   Trying to start anyway..." -ForegroundColor Yellow
}

# Set environment variables
$env:PORT = "3000"
$env:BROWSER = "none"  # Don't auto-open browser

Write-Host "`n✅ Starting React development server..." -ForegroundColor Green
Write-Host "   Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Registration: http://localhost:3000/#/register" -ForegroundColor Cyan
Write-Host "   Login: http://localhost:3000/#/login" -ForegroundColor Cyan
Write-Host "`n" + "=" * 50
Write-Host ""

# Start the server
npm start

