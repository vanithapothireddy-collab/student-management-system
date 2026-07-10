from pydantic import BaseModel

class BatchCreate(BaseModel):

    batch_name: str
    year: int