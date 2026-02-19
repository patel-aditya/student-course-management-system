from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Foreign key to teacher(User table)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to User (teacher)
    teacher = relationship("User", back_populates="courses")

    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")