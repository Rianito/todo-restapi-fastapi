from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskModel(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
    finished: bool


class CreateTaskModel(BaseModel):
    title: str
    description: str


class UpdateTaskModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    finished: Optional[bool]
