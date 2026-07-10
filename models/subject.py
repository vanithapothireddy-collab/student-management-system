from pydantic import BaseModel

class SubjectCreate(BaseModel):

    subject_name: str