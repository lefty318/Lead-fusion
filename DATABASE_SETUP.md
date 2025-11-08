# Database Setup Guide

This guide will help you configure PostgreSQL for the OmniLead project.

## Prerequisites

- PostgreSQL installed and running
- PostgreSQL service started
- Admin access to PostgreSQL

## Step 1: Install PostgreSQL (If Not Installed)

### Windows Installation

1. **Download PostgreSQL:**
   - Visit: https://www.postgresql.org/download/windows/
   - Download the installer from EnterpriseDB or use the official installer
   - Recommended: PostgreSQL 14 or newer

2. **Install:**
   - Run the installer
   - Remember the password you set for the `postgres` user
   - Default port: `5432`
   - Default installation path: `C:\Program Files\PostgreSQL\XX`

3. **Verify Installation:**
   ```powershell
   # Check if PostgreSQL service is running
   Get-Service postgresql*
   
   # Or check in Services (services.msc)
   # Look for "postgresql-x64-XX" service
   ```

### Alternative: Using Chocolatey

```powershell
# Run as Administrator
choco install postgresql -y
```

## Step 2: Start PostgreSQL Service

### Check Service Status

```powershell
# Check if PostgreSQL is running
Get-Service postgresql*

# If not running, start it
Start-Service postgresql-x64-XX  # Replace XX with your version
```

### Or Start Manually

1. Press `Win + R`
2. Type `services.msc`
3. Find `postgresql-x64-XX`
4. Right-click → Start

## Step 3: Access PostgreSQL

### Using psql (Command Line)

```powershell
# Connect to PostgreSQL
psql -U postgres

# If psql is not in PATH, use full path:
# "C:\Program Files\PostgreSQL\XX\bin\psql.exe" -U postgres
```

### Using pgAdmin (GUI Tool)

- pgAdmin is usually installed with PostgreSQL
- Launch from Start Menu
- Connect using the password you set during installation

## Step 4: Create Database

### Option A: Using psql Command Line

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE omnilead;

-- Create a dedicated user (optional but recommended)
CREATE USER omnilead_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE omnilead TO omnilead_user;

-- Connect to the new database
\c omnilead

-- Grant schema privileges (if using the user)
GRANT ALL ON SCHEMA public TO omnilead_user;

-- Exit
\q
```

### Option B: Using pgAdmin

1. Open pgAdmin
2. Connect to PostgreSQL server
3. Right-click "Databases" → "Create" → "Database"
4. Name: `omnilead`
5. Owner: `postgres` (or your user)
6. Click "Save"

### Option C: Using SQL Script

Create a file `create_database.sql`:

```sql
-- Create database
CREATE DATABASE omnilead
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Create user (optional)
CREATE USER omnilead_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE omnilead TO omnilead_user;
```

Run it:
```powershell
psql -U postgres -f create_database.sql
```

## Step 5: Configure .env File

Edit `backend/.env` file:

```env
# Database Configuration
# Format: postgresql://username:password@host:port/database

# Option 1: Using postgres superuser (development only)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/omnilead

# Option 2: Using dedicated user (recommended)
DATABASE_URL=postgresql://omnilead_user:your_secure_password@localhost:5432/omnilead

# Option 3: If PostgreSQL is on different host/port
DATABASE_URL=postgresql://username:password@hostname:5432/omnilead
```

### Example Values

**Development (local):**
```env
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/omnilead
```

**With dedicated user:**
```env
DATABASE_URL=postgresql://omnilead_user:securepass123@localhost:5432/omnilead
```

**Remote database:**
```env
DATABASE_URL=postgresql://user:pass@192.168.1.100:5432/omnilead
```

## Step 6: Test Database Connection

### Using Python

```powershell
cd backend
python -c "from app.config import settings; from sqlalchemy import create_engine; engine = create_engine(settings.database_url); conn = engine.connect(); print('✅ Database connection successful!'); conn.close()"
```

### Using psql

```powershell
psql -U postgres -d omnilead
# If successful, you'll see: omnilead=#
```

## Step 7: Run Database Migrations

Once the database is created and configured:

```powershell
cd backend

# Create initial migration
python -m alembic revision --autogenerate -m "Initial migration"

# Review the generated migration file in alembic/versions/

# Apply migration
python -m alembic upgrade head
```

## Step 8: Verify Tables Created

### Using psql

```sql
-- Connect to database
psql -U postgres -d omnilead

-- List all tables
\dt

-- Describe a table
\d users
\d conversations
\d messages
```

### Using Python

```python
from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables:", tables)
```

## Troubleshooting

### Connection Refused

**Error**: `could not connect to server: Connection refused`

**Solutions**:
1. Check PostgreSQL service is running:
   ```powershell
   Get-Service postgresql*
   ```
2. Verify port 5432 is not blocked by firewall
3. Check PostgreSQL is listening:
   ```powershell
   netstat -an | findstr 5432
   ```

### Authentication Failed

**Error**: `password authentication failed`

**Solutions**:
1. Verify password in `.env` matches PostgreSQL password
2. Check `pg_hba.conf` file (usually in `C:\Program Files\PostgreSQL\XX\data\`)
3. Reset password if needed:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

### Database Does Not Exist

**Error**: `database "omnilead" does not exist`

**Solution**:
```sql
CREATE DATABASE omnilead;
```

### Permission Denied

**Error**: `permission denied for schema public`

**Solution**:
```sql
GRANT ALL ON SCHEMA public TO your_username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_username;
```

### Port Already in Use

**Error**: Port 5432 already in use

**Solutions**:
1. Find what's using the port:
   ```powershell
   netstat -ano | findstr :5432
   ```
2. Change PostgreSQL port in `postgresql.conf`
3. Update `DATABASE_URL` with new port

## Quick Setup Script

Create `setup_database.ps1`:

```powershell
# Run as Administrator
$dbName = "omnilead"
$dbUser = "postgres"
$dbPassword = Read-Host "Enter PostgreSQL password for $dbUser" -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

# Create database
$env:PGPASSWORD = $dbPasswordPlain
& "C:\Program Files\PostgreSQL\XX\bin\psql.exe" -U $dbUser -c "CREATE DATABASE $dbName;" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database '$dbName' created successfully"
} else {
    Write-Host "⚠️  Database might already exist or error occurred"
}

# Update .env file
$envFile = "backend\.env"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    $newUrl = "DATABASE_URL=postgresql://$dbUser`:$dbPasswordPlain@localhost:5432/$dbName"
    
    if ($content -match "DATABASE_URL=.*") {
        $content = $content -replace "DATABASE_URL=.*", $newUrl
    } else {
        $content += "`n$newUrl"
    }
    
    Set-Content $envFile $content
    Write-Host "✅ Updated .env file with database URL"
} else {
    Write-Host "⚠️  .env file not found"
}

Write-Host "`nNext steps:"
Write-Host "1. Run migrations: cd backend && python -m alembic upgrade head"
Write-Host "2. Start server: python -m uvicorn app.main:socket_app --reload"
```

## Security Best Practices

1. **Use dedicated database user** (not `postgres` superuser)
2. **Strong passwords** for database users
3. **Limit network access** (use `localhost` for development)
4. **Regular backups** of your database
5. **Don't commit `.env` files** to version control

## Next Steps

After database is configured:

1. ✅ Database created
2. ✅ `.env` file updated with `DATABASE_URL`
3. ✅ Connection tested
4. ⬜ Run migrations: `python -m alembic upgrade head`
5. ⬜ Start backend server
6. ⬜ Verify tables created

---

**Need help?** Check the troubleshooting section or verify your PostgreSQL installation.

