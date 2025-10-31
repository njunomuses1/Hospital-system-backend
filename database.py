from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from config import settings

# Parse DATABASE_URL and URL-encode password if needed
def prepare_database_url(url: str) -> str:
    """Prepare database URL with proper password encoding"""
    # If URL already has @, split and encode password part
    if '@' in url and '://' in url:
        parts = url.split('://', 1)
        if len(parts) == 2:
            scheme = parts[0]
            rest = parts[1]
            if '@' in rest:
                auth_and_host = rest.split('@', 1)
                if ':' in auth_and_host[0]:
                    user_pass = auth_and_host[0].split(':', 1)
                    if len(user_pass) == 2:
                        user = user_pass[0]
                        password = user_pass[1]
                        host_db = auth_and_host[1]
                        # URL encode password
                        encoded_password = quote_plus(password)
                        return f"{scheme}://{user}:{encoded_password}@{host_db}"
    return url

# Create database engine with URL-encoded password
database_url = prepare_database_url(settings.DATABASE_URL)

# Configure SSL for managed MySQL providers (e.g., Railway) when enabled
engine_kwargs = dict(
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600,
)

if database_url.startswith("mysql+pymysql://") and settings.DATABASE_SSL:
    # PyMySQL enables TLS when an 'ssl' dict is provided
    engine_kwargs["connect_args"] = {"ssl": {}}

engine = create_engine(
    database_url,
    **engine_kwargs,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Database initialization failed: {error_msg}")
        if "Access denied" in error_msg:
            print("\n💡 MySQL Connection Error - Possible solutions:")
            print("   1. Verify MySQL root password in backend/.env")
            print("   2. Make sure MySQL service is running")
            print("   3. Check if database 'hospital_db' exists")
            print("   4. Run: setup-database.bat or connect-mysql.bat")
        raise







