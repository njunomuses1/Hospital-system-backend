"""
Setup script for Hospital Management System Backend
"""
import os
import sys
import subprocess


def create_venv():
    """Create virtual environment"""
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        pip_path = "venv\\Scripts\\pip" if os.name == "nt" else "venv/bin/pip"
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from example"""
    if os.path.exists(".env"):
        print("\n⚠️  .env file already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            return True
    
    print("\n📝 Creating .env file...")
    print("\nPlease provide your database credentials:")
    
    db_user = input("MySQL username (default: root): ") or "root"
    db_password = input("MySQL password: ")
    db_host = input("MySQL host (default: localhost): ") or "localhost"
    db_port = input("MySQL port (default: 3306): ") or "3306"
    db_name = input("Database name (default: hospital_db): ") or "hospital_db"
    
    database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    env_content = f"""# Database Configuration
DATABASE_URL={database_url}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Application
APP_NAME=Hospital Management System
VERSION=1.0.0
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def create_database():
    """Create MySQL database"""
    print("\n💾 Creating MySQL database...")
    response = input("Do you want to create the database now? (Y/n): ")
    
    if response.lower() == 'n':
        print("⚠️  Please create the database manually:")
        print("   CREATE DATABASE hospital_db;")
        return True
    
    try:
        import pymysql
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Parse database URL
        db_url = os.getenv("DATABASE_URL")
        # Extract connection info (simplified)
        
        print("⚠️  Please create the database manually using:")
        print("   CREATE DATABASE hospital_db;")
        return True
        
    except ImportError:
        print("⚠️  pymysql not yet installed. Please create database manually:")
        print("   CREATE DATABASE hospital_db;")
        return True


def seed_database():
    """Seed database with sample data"""
    print("\n🌱 Seeding database with sample data...")
    response = input("Do you want to seed the database? (Y/n): ")
    
    if response.lower() == 'n':
        print("Skipping seed...")
        return True
    
    try:
        python_path = "venv\\Scripts\\python" if os.name == "nt" else "venv/bin/python"
        subprocess.run([python_path, "seed_data.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to seed database")
        print("You can seed later by running: python seed_data.py")
        return False


def main():
    """Main setup function"""
    print("""
╔═══════════════════════════════════════════╗
║  Hospital Management System - Setup       ║
║  FastAPI Backend Configuration            ║
╚═══════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected\n")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not create_venv():
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create database
    create_database()
    
    # Seed database
    seed_database()
    
    print("""
╔═══════════════════════════════════════════╗
║  🎉 Setup Complete!                       ║
╚═══════════════════════════════════════════╝

Next steps:
1. Make sure MySQL is running
2. Ensure database 'hospital_db' exists
3. Run the backend:
   
   Windows: run.bat
   Linux/Mac: ./run.sh
   
   Or manually:
   - Activate venv: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)
   - Run: python main.py

4. API will be available at: http://localhost:8000
5. Documentation: http://localhost:8000/docs

Happy coding! 🚀
    """)


if __name__ == "__main__":
    main()
















