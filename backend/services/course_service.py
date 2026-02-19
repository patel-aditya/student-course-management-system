from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.course import Course
from schemas.course import CourseCreate, CourseUpdate
from models.user import User


class CourseService:

    @staticmethod
    def create_course(db: Session, course_data: CourseCreate, teacher: User):
        new_course = Course(
            title=course_data.title,
            description=course_data.description,
            teacher_id=teacher.id
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        return new_course

    @staticmethod
    def get_course_by_id(db: Session, course_id: int):
        course = db.query(Course).filter(Course.id == course_id).first()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        return course

    @staticmethod
    def update_course(db: Session, course: Course, update_data: CourseUpdate):
        if update_data.title is not None:
            course.title = update_data.title

        if update_data.description is not None:
            course.description = update_data.description

        db.commit()
        db.refresh(course)

        return course

    @staticmethod
    def delete_course(db: Session, course: Course):
        db.delete(course)
        db.commit()
