from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db

from models.enrollment import Enrollment
from models.course import Course
from models.user import User
from schemas.enrollment import EnrollmentOut, EnrollmentBase, GradeUpdate
from dependencies import require_role, get_current_user
from enums.roles import UserRole


router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentBase, status_code=status.HTTP_201_CREATED)
def enroll_in_course(enrollment: EnrollmentBase, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.student))):
    # check if course exists
    db_course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course Not found")
    
    # prevent duplicate enrollment
    existing = db.query(Enrollment).filter(Enrollment.student_id == current_user.id, Enrollment.course_id == enrollment.course_id).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Already Enrolled in this course")
    
    new_enrollment = Enrollment(student_id = current_user.id, course_id = enrollment.course_id)

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


@router.get("/me", response_model=List[EnrollmentOut])
def get_my_enrollment(db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.student))):
    return db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()


@router.patch("/{enrollment_id}/grade", response_model=EnrollmentOut)
def assign_grade(enrollment_id:int, grade_data: GradeUpdate, db:Session= Depends(get_db), current_user: User = Depends(require_role(UserRole.teacher))):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    
    # check if the teacher owns the course
    if enrollment.course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to assign grade for this enrollment")
    
    enrollment.grade = grade_data.grade
    db.commit()
    db.refresh(enrollment)

    return enrollment