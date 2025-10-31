"""Test MySQL connection"""
from config import settings
from database import engine

print("=" * 50)
print("Testing Database Connection")
print("=" * 50)
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print()

try:
    # Try to connect
    with engine.connect() as conn:
        print("✅ Connection successful!")
        
        # Check if database exists
        result = conn.execute("SHOW DATABASES LIKE 'hospital_db'")
        db_exists = result.fetchone()
        
        if db_exists:
            print("✅ Database 'hospital_db' exists")
        else:
            print("❌ Database 'hospital_db' does NOT exist")
            print("   Run: CREATE DATABASE hospital_db;")
            
        # Try to use the database
        conn.execute("USE hospital_db")
        print("✅ Can access 'hospital_db' database")
        
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"   Error: {type(e).__name__}: {str(e)}")
    print()
    print("Possible issues:")
    print("1. MySQL service not running")
    print("2. Wrong password")
    print("3. Database doesn't exist")
    print("4. User doesn't have permissions")








