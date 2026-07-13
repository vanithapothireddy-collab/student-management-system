from pydantic import BaseModel

class TeacherCreate(BaseModel):
    teacher_name: str
    subject_name: str
    email: str