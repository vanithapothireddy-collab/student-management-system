from pydantic import BaseModel

class TeacherSubjectCreate(BaseModel):
    teacher_id: int
    subject_id: int