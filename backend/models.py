from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime, timezone

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Todo {self.id} {self.task} {self.is_done} {self.created_at} {self.updated_at} {self.completed_at}>"
    