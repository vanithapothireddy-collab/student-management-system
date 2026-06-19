from pydantic import BaseModel, Field

class StudentCreate(BaseModel):

    student_name: str = Field(
        min_length=3,
        max_length=100
    )

    gender: str = Field(
        min_length=1,
        max_length=1
    )

    department_id: int = Field(
        gt=0
    )

    batch_id: int = Field(
        gt=0
    )