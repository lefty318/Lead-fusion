#!/usr/bin/env python
"""
Database Configuration Helper
This script helps configure and test the database connection
"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError

def get_env_file():
    """Get the .env file path"""
    return Path(__file__).parent / '.env'

def read_env_file():
    """Read current .env file"""
    env_file = get_env_file()
    if not env_file.exists():
        return {}
    
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def update_env_file(key, value):
    """Update a value in .env file"""
    env_file = get_env_file()
    env_vars = read_env_file()
    env_vars[key] = value
    
    # Read existing file to preserve comments
    lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Update or add the key
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f'{key}='):
            lines[i] = f'{key}={value}\n'
            updated = True
            break
    
    if not updated:
        lines.append(f'{key}={value}\n')
    
    with open(env_file, 'w') as f:
        f.writelines(lines)

def test_connection(database_url):
    """Test database connection"""
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"   PostgreSQL version: {version.split(',')[0]}")
            return True
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_database_exists(database_url, db_name):
    """Check if database exists"""
    try:
        # Connect to postgres database to check
        base_url = database_url.rsplit('/', 1)[0]
        engine = create_engine(f"{base_url}/postgres")
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            exists = result.fetchone() is not None
            return exists
    except Exception as e:
        print(f"⚠️  Could not check if database exists: {e}")
        return None

def list_databases(database_url):
    """List all databases"""
    try:
        base_url = database_url.rsplit('/', 1)[0]
        engine = create_engine(f"{base_url}/postgres")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false"))
            databases = [row[0] for row in result.fetchall()]
            return databases
    except Exception as e:
        print(f"⚠️  Could not list databases: {e}")
        return []

def create_database(database_url, db_name):
    """Create database"""
    try:
        base_url = database_url.rsplit('/', 1)[0]
        engine = create_engine(f"{base_url}/postgres")
        with engine.connect() as conn:
            # Set autocommit for CREATE DATABASE
            conn.execute(text("COMMIT"))
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            conn.commit()
        print(f"✅ Database '{db_name}' created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def main():
    """Main configuration function"""
    print("🗄️  OmniLead Database Configuration\n")
    print("=" * 50)
    
    # Read current configuration
    env_vars = read_env_file()
    current_url = env_vars.get('DATABASE_URL', '')
    
    if current_url:
        print(f"\n📋 Current DATABASE_URL: {current_url}")
    else:
        print("\n⚠️  No DATABASE_URL found in .env file")
    
    # Get database configuration
    print("\n📝 Database Configuration")
    print("-" * 50)
    
    # Parse current URL if exists
    if current_url and current_url.startswith('postgresql://'):
        try:
            # Format: postgresql://user:password@host:port/database
            parts = current_url.replace('postgresql://', '').split('@')
            if len(parts) == 2:
                user_pass = parts[0].split(':')
                host_db = parts[1].split('/')
                host_port = host_db[0].split(':')
                
                current_user = user_pass[0] if len(user_pass) > 0 else 'postgres'
                current_host = host_port[0] if len(host_port) > 0 else 'localhost'
                current_port = host_port[1] if len(host_port) > 1 else '5432'
                current_db = host_db[1] if len(host_db) > 1 else 'omnilead'
            else:
                current_user = 'postgres'
                current_host = 'localhost'
                current_port = '5432'
                current_db = 'omnilead'
        except:
            current_user = 'postgres'
            current_host = 'localhost'
            current_port = '5432'
            current_db = 'omnilead'
    else:
        current_user = 'postgres'
        current_host = 'localhost'
        current_port = '5432'
        current_db = 'omnilead'
    
    # Get user input
    print(f"\nEnter database configuration (press Enter to use defaults):")
    user = input(f"Username [{current_user}]: ").strip() or current_user
    password = input(f"Password: ").strip()
    host = input(f"Host [{current_host}]: ").strip() or current_host
    port = input(f"Port [{current_port}]: ").strip() or current_port
    database = input(f"Database name [{current_db}]: ").strip() or current_db
    
    if not password:
        print("⚠️  Password is required!")
        sys.exit(1)
    
    # Build 
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    print(f"\n🔗 Testing connection...")
    print(f"   URL: postgresql://{user}:***@{host}:{port}/{database}")
    
    # Test connection to postgres database first
    test_url = f"postgresql://{user}:{password}@{host}:{port}/postgres"
    if not test_connection(test_url):
        print("\n❌ Cannot connect to PostgreSQL server")
        print("   Please check:")
        print("   1. PostgreSQL is installed and running")
        print("   2. Username and password are correct")
        print("   3. Host and port are correct")
        print("   4. PostgreSQL service is started")
        sys.exit(1)
    
    # Check if target database exists
    print(f"\n🔍 Checking if database '{database}' exists...")
    db_exists = check_database_exists(test_url, database)
    
    if db_exists is False:
        print(f"⚠️  Database '{database}' does not exist")
        create = input(f"   Create database '{database}'? (y/n): ").strip().lower()
        if create == 'y':
            if create_database(test_url, database):
                print(f"✅ Database '{database}' created")
            else:
                print("❌ Failed to create database")
                sys.exit(1)
        else:
            print("❌ Database must exist to continue")
            sys.exit(1)
    elif db_exists:
        print(f"✅ Database '{database}' exists")
    
    # Test connection to target database
    print(f"\n🔗 Testing connection to database '{database}'...")
    if test_connection(database_url):
        # Update .env file
        update_env_file('DATABASE_URL', database_url)
        print(f"\n✅ Database configuration saved to .env file")
        
        # List tables if any exist
        try:
            engine = create_engine(database_url)
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if tables:
                print(f"\n📊 Found {len(tables)} table(s) in database:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print(f"\n📊 Database is empty (no tables yet)")
                print(f"   Run migrations to create tables:")
                print(f"   python -m alembic revision --autogenerate -m 'Initial migration'")
                print(f"   python -m alembic upgrade head")
        except Exception as e:
            print(f"⚠️  Could not list tables: {e}")
        
        print("\n" + "=" * 50)
        print("\n✅ Database configuration complete!")
        print("\n📝 Next steps:")
        print("   1. Run migrations: python -m alembic upgrade head")
        print("   2. Start server: python -m uvicorn app.main:socket_app --reload")
    else:
        print(f"\n❌ Cannot connect to database '{database}'")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

