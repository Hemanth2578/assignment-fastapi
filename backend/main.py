from fastapi import FastAPI, HTTPException, Depends, status
from models import Todo, Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas import TodoCreate, TodoUpdate, TodoResponse
from datetime import datetime, timezone
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine) # Drop the existing table
Base.metadata.create_all(bind=engine) # create tables if not exists

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        new_todo = Todo(**todo.dict())
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/todos/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()  

@app.get("/todos/{id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_to_do(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo  

@app.put("/todos/{id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.task = todo.task
    db_todo.is_done = todo.is_done
    db_todo.completed_at = datetime.now(timezone.utc) if todo.is_done else None
    db_todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return None