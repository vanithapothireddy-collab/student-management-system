from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    department_name: str