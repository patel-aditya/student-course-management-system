from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

# 🔹 Database configuration

DATABASE_URL = "postgresql://postgres:Aditya%407879%40DataBase@localhost:5432/student-db"
# Change username, password, db name accordingly


# 🔹 Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL queries in console (good for development)
)


# 🔹 Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 🔹 Base class for models
Base = declarative_base()


# 🔹 Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
