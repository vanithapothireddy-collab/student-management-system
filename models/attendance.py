from pydantic import BaseModel
from datetime import date

class AttendanceCreate(BaseModel):

    student_id: int
    subject_id: int
    attendance_date: date
    status: str