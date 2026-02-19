from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.course import Course
from models.user import User    
from schemas.course import CourseCreate, CourseOut
from dependencies import require_role
from enums.roles import UserRole

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db),current_user: User = Depends(require_role(UserRole.teacher))):
    new_course = Course(title=course.title, description=course.description, teacher_id=current_user.id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/", response_model=  List[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()

    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return db_course
