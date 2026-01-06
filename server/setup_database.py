"""
Database setup script for NED University Document Management System
Creates the database and initializes tables
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from config import get_settings

def create_database():
    """Create the database if it doesn't exist."""
    settings = get_settings()
    
    # Parse database URL to get connection details
    # Format: postgresql://user:password@host:port/database
    db_url = settings.database_url
    
    # Extract connection details
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', '')
    
    # Split into parts
    try:
        # user:password@host:port/database
        auth_host = db_url.split('@')
        user_pass = auth_host[0].split(':')
        username = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ''
        
        host_db = auth_host[1].split('/')
        host_port = host_db[0].split(':')
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else '5432'
        database = host_db[1] if len(host_db) > 1 else 'ned_university_docs'
        
        print(f"Connecting to PostgreSQL at {host}:{port}...")
        
        # Connect to PostgreSQL server (postgres database)
        conn = psycopg2.connect(
            dbname='postgres',
            user=username,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"✓ Database '{database}' already exists")
        else:
            print(f"Creating database '{database}'...")
            cursor.execute(f'CREATE DATABASE "{database}"')
            print(f"✓ Database '{database}' created successfully")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. Your DATABASE_URL in .env is correct")
        print("3. The PostgreSQL user has permission to create databases")
        return False

def initialize_tables():
    """Initialize database tables using SQLAlchemy."""
    print("\nInitializing database tables...")
    try:
        from database import engine, Base
        from models import Student  # Import models to register them
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        # Print created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {', '.join(tables)}")
        
        return True
        
    except Exception as e:
        print(f"Error initializing tables: {str(e)}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("NED University Document Management System")
    print("Database Setup")
    print("=" * 60)
    print()
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Database creation failed")
        sys.exit(1)
    
    # Step 2: Create tables
    if not initialize_tables():
        print("\n❌ Table initialization failed")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print()
    print("You can now start the server with: python main.py")
    print()

if __name__ == "__main__":
    main()
