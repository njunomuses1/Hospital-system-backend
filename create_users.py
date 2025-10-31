"""
Script to create initial users for Hospital Management System
Run this after setting up the database
"""
from database import SessionLocal, init_db
from auth import get_password_hash
import models
from datetime import datetime


def create_initial_users():
    """Create initial admin and sample users"""
    
    # Initialize database (create tables if they don't exist)
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if any users exist
        existing_users = db.query(models.User).count()
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} user(s)")
            response = input("Do you want to add more users? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        print("\n" + "="*50)
        print("Creating Initial Users")
        print("="*50 + "\n")
        
        # Define users to create
        users_to_create = [
            {
                "username": "admin",
                "email": "admin@hospital.com",
                "password": "admin123",
                "full_name": "System Administrator",
                "role": "admin"
            },
            {
                "username": "doctor1",
                "email": "doctor1@hospital.com",
                "password": "doctor123",
                "full_name": "Dr. John Smith",
                "role": "doctor"
            },
            {
                "username": "staff1",
                "email": "staff1@hospital.com",
                "password": "staff123",
                "full_name": "Jane Doe",
                "role": "staff"
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        for user_data in users_to_create:
            # Check if user already exists
            existing = db.query(models.User).filter(
                (models.User.email == user_data["email"]) | 
                (models.User.username == user_data["username"])
            ).first()
            
            if existing:
                print(f"⏭️  Skipped: {user_data['username']} (already exists)")
                skipped_count += 1
                continue
            
            # Create new user
            hashed_password = get_password_hash(user_data["password"])
            new_user = models.User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                full_name=user_data["full_name"],
                role=user_data["role"],
                is_active=True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"✅ Created: {user_data['username']} ({user_data['role']}) - {user_data['email']}")
            created_count += 1
        
        print("\n" + "="*50)
        print(f"✅ Created {created_count} user(s)")
        if skipped_count > 0:
            print(f"⏭️  Skipped {skipped_count} user(s) (already existed)")
        print("="*50 + "\n")
        
        if created_count > 0:
            print("Default Login Credentials:")
            print("-" * 50)
            print("Admin:")
            print("  Email: admin@hospital.com")
            print("  Password: admin123")
            print("\nDoctor:")
            print("  Email: doctor1@hospital.com")
            print("  Password: doctor123")
            print("\nStaff:")
            print("  Email: staff1@hospital.com")
            print("  Password: staff123")
            print("-" * 50)
            print("\n⚠️  IMPORTANT: Change these passwords in production!\n")
        
    except Exception as e:
        print(f"\n❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()


def create_custom_user():
    """Create a custom user with interactive prompts"""
    init_db()
    db = SessionLocal()
    
    try:
        print("\n" + "="*50)
        print("Create Custom User")
        print("="*50 + "\n")
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username is required")
            return
        
        email = input("Email: ").strip()
        if not email:
            print("❌ Email is required")
            return
        
        password = input("Password: ").strip()
        if not password:
            print("❌ Password is required")
            return
        
        full_name = input("Full Name (optional): ").strip() or None
        
        print("\nRole Options:")
        print("1. admin")
        print("2. doctor")
        print("3. staff")
        role_choice = input("Select role (1-3): ").strip()
        
        role_map = {"1": "admin", "2": "doctor", "3": "staff"}
        role = role_map.get(role_choice, "staff")
        
        # Check if user exists
        existing = db.query(models.User).filter(
            (models.User.email == email) | 
            (models.User.username == username)
        ).first()
        
        if existing:
            print(f"\n❌ User with email '{email}' or username '{username}' already exists")
            return
        
        # Create user
        hashed_password = get_password_hash(password)
        new_user = models.User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("\n" + "="*50)
        print(f"✅ User created successfully!")
        print("="*50)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Full Name: {full_name or 'N/A'}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()


def list_users():
    """List all users in the database"""
    db = SessionLocal()
    
    try:
        users = db.query(models.User).all()
        
        if not users:
            print("\n📭 No users found in database")
            return
        
        print("\n" + "="*70)
        print(f"Total Users: {len(users)}")
        print("="*70)
        print(f"{'Username':<15} {'Email':<30} {'Role':<10} {'Active':<10}")
        print("-"*70)
        
        for user in users:
            active = "✅ Yes" if user.is_active else "❌ No"
            print(f"{user.username:<15} {user.email:<30} {user.role:<10} {active:<10}")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error listing users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Hospital Management System - User Management")
    print("="*50 + "\n")
    
    print("Options:")
    print("1. Create default users (admin, doctor, staff)")
    print("2. Create custom user")
    print("3. List all users")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        create_initial_users()
    elif choice == "2":
        create_custom_user()
    elif choice == "3":
        list_users()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid option")














