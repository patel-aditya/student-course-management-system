from pydantic import BaseModel
from typing import Optional 
from schemas.course import CourseOut


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class GradeUpdate(BaseModel):
    grade: str

class EnrollmentOut(EnrollmentBase):
    id: int
    course_id: int
    student_id: int
    grade: Optional[str]
    course: CourseOut

    class Config:
        from_attributes = True