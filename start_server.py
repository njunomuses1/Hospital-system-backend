"""Simple server startup script with error handling"""
import sys
import traceback

print("=" * 50)
print("Starting Hospital Management System Backend")
print("=" * 50)

try:
    print("\n[1/6] Importing FastAPI...")
    from fastapi import FastAPI
    print("✅ FastAPI imported")
    
    print("\n[2/6] Importing uvicorn...")
    import uvicorn
    print("✅ Uvicorn imported")
    
    print("\n[3/6] Importing config...")
    from config import settings
    print(f"✅ Config loaded - Database: {settings.DATABASE_URL}")
    
    print("\n[4/6] Importing database...")
    from database import init_db
    print("✅ Database module imported")
    
    print("\n[5/6] Importing main app...")
    from main import app
    print("✅ Main app imported")
    
    print("\n[6/6] Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    print("\n" + "=" * 50)
    print("🚀 Starting server...")
    print(f"📍 API: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📖 Docs: http://localhost:{settings.API_PORT}/docs")
    print("=" * 50 + "\n")
    
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False  # Disable reload for stability
    )
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    print("\nFull traceback:")
    print("=" * 50)
    traceback.print_exc()
    print("=" * 50)
    sys.exit(1)













