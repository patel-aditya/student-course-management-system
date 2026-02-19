from pydantic import BaseModel
from typing import Optional
from schemas.user import UserOut

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CourseOut(CourseBase):
    id: int
    teacher_id: int
    teacher: UserOut

    class Config:
        from_attributes = True