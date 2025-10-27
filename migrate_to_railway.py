"""
Script to migrate database to Railway
"""
import sys
from sqlalchemy import create_engine, text, inspect
from database import engine, Base, init_db
from config import settings
from models import User, Patient, Doctor, Appointment, Prescription

def test_connection():
    """Test the database connection"""
    print("=" * 60)
    print("Testing Railway Database Connection")
    print("=" * 60)
    print(f"\nDatabase URL: {settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('//')[1], '***')}")
    
    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection successful!")
            
            # Get database info
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"✅ Connected to database: {db_name}")
            
            # Get MySQL version
            result = conn.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"✅ MySQL version: {version}")
            
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def check_existing_tables():
    """Check if tables already exist"""
    print("\n" + "=" * 60)
    print("Checking Existing Tables")
    print("=" * 60)
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"\n✅ Found {len(tables)} existing tables:")
            for table in tables:
                print(f"   - {table}")
            return True
        else:
            print("\nℹ️  No existing tables found")
            return False
    except Exception as e:
        print(f"❌ Error checking tables: {str(e)}")
        return False

def create_tables():
    """Create all tables in the Railway database"""
    print("\n" + "=" * 60)
    print("Creating Database Tables")
    print("=" * 60)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Successfully created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

def seed_initial_data():
    """Seed database with initial data"""
    print("\n" + "=" * 60)
    print("Seeding Initial Data")
    print("=" * 60)
    
    from seed_data import seed_database
    
    try:
        result = seed_database()
        if result:
            print("\n✅ Database seeded successfully!")
            return True
        else:
            print("\n❌ Failed to seed database")
            return False
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        return False

def main():
    """Main migration function"""
    print("\n" + "=" * 60)
    print("🚀 Railway Database Migration Tool")
    print("=" * 60)
    
    # Step 1: Test connection
    if not test_connection():
        print("\n❌ Migration aborted: Cannot connect to Railway database")
        print("\nPlease check:")
        print("  1. Your internet connection")
        print("  2. The DATABASE_URL in your .env file")
        print("  3. Railway database is running")
        sys.exit(1)
    
    # Step 2: Check existing tables
    has_tables = check_existing_tables()
    
    if has_tables:
        print("\n⚠️  Warning: Tables already exist!")
        response = input("\nDo you want to recreate tables? (This will DROP all data) [yes/NO]: ")
        if response.lower() == 'yes':
            print("\nDropping existing tables...")
            Base.metadata.drop_all(bind=engine)
            print("✅ Tables dropped")
        else:
            print("\n✅ Keeping existing tables")
            return
    
    # Step 3: Create tables
    if not create_tables():
        print("\n❌ Migration aborted: Cannot create tables")
        sys.exit(1)
    
    # Step 4: Seed data
    response = input("\nDo you want to seed the database with sample data? [YES/no]: ")
    if response.lower() != 'no':
        seed_initial_data()
    
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print("\nYour Railway database is ready to use!")
    print(f"\nBackend will connect to: {settings.DATABASE_URL.split('@')[1]}")
    print("\nNext steps:")
    print("  1. Start your backend: python main.py")
    print("  2. Test the API: http://localhost:8000/docs")
    print("  3. Deploy your backend to Railway")

if __name__ == "__main__":
    main()

