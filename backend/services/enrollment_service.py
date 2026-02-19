from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.enrollment import Enrollment
from models.course import Course
from models.user import User


class EnrollmentService:

    @staticmethod
    def enroll_student(db: Session, student: User, course_id: int):

        # Check course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        # Prevent duplicate
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already enrolled in this course"
            )

        enrollment = Enrollment(
            student_id=student.id,
            course_id=course_id
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

        return enrollment

    @staticmethod
    def assign_grade(db: Session, teacher: User, enrollment_id: int, grade: str):

        enrollment = db.query(Enrollment).filter(
            Enrollment.id == enrollment_id
        ).first()

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )

        # Ownership validation
        if enrollment.course.teacher_id != teacher.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only grade your own courses"
            )

        enrollment.grade = grade

        db.commit()
        db.refresh(enrollment)

        return enrollment
