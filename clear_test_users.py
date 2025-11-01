"""
Clear test users from the database
Run this if you want to start fresh with user registration
"""
from database import SessionLocal
import models

def clear_test_users():
    """Delete all test users (keeps sample data doctors/patients)"""
    db = SessionLocal()
    try:
        # List common test usernames/emails
        test_patterns = ['test', 'demo', 'sample', 'newuser']
        
        users = db.query(models.User).all()
        deleted_count = 0
        
        print("Current users in database:")
        for user in users:
            print(f"  - {user.username} ({user.email})")
        
        print("\nDo you want to delete ALL users? (yes/no): ", end='')
        response = input().strip().lower()
        
        if response == 'yes':
            count = db.query(models.User).delete()
            db.commit()
            print(f"\n✅ Deleted {count} users")
            print("You can now register fresh users!")
        else:
            print("\n❌ Cancelled. No users were deleted.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Clear Test Users")
    print("=" * 50)
    print()
    clear_test_users()















