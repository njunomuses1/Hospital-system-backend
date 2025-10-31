"""
Initialize the database - create database and tables
"""
import pymysql
from sqlalchemy import create_engine, text
from database import Base, engine
import models

def create_database():
    """Create the hospital_db database if it doesn't exist"""
    try:
        # Connect to MySQL without specifying database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
            print("✅ Database 'hospital_db' created/verified")
        
        connection.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("\nPlease ensure:")
        print("1. MySQL is running")
        print("2. MySQL root password is 'password' (or update config.py)")
        raise

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    print("====================================")
    print("Hospital Management System")
    print("Database Initialization")
    print("====================================\n")
    
    print("Step 1: Creating database...")
    create_database()
    
    print("\nStep 2: Creating tables...")
    create_tables()
    
    print("\n✅ Database initialization complete!")
    print("\nYou can now:")
    print("1. Run 'python main.py' to start the backend server")
    print("2. Run 'python create_users.py' to create test users")













