from sqlalchemy import Column, Integer, String, Enum
from database import Base
from sqlalchemy.orm import relationship
from backend.enums.roles import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))

    # one student -> many enrollments
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")