from pydantic import BaseModel

class FeeCreate(BaseModel):
    student_id: int
    total_fee: float
    paid_fee: float
    status: str