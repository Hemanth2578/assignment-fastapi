from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    task: str = Field(..., description="Task must not be blank")

    @field_validator("task")
    @classmethod
    def task_must_not_be_blank(cls, v):
        if v.isspace() or v is None:
            raise ValueError("Task must not be blank")
        return v

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    task: Optional[str] = Field(None, description="Task must not be blank")
    is_done: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    is_done: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%B %d, %Y %I:%M %p")  # Example: "January 14, 2025 11:11 AM"
        }