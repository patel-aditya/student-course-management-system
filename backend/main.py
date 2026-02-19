from fastapi import FastAPI

from database import Base, engine

# Import all models so SQLAlchemy can register them
from models import user, course, enrollment

# Import routers
from routers import courses, enrollments, users


# Create FastAPI instance
app = FastAPI(
    title="Student Course Management API",
    description="Level 2 Backend Project using FastAPI",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(users.router)


# Root endpoint (health check)
@app.get("/")
def root():
    return {"message": "Student Course Management API is running"}
