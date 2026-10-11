from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.db.schemas.todo_schema import TodoSchema
from sqlalchemy import select
from app.dependencies import authenticate_user

router = APIRouter(
    prefix="/todo",
    dependencies=[Depends(authenticate_user)]
)

@router.get("/")
def index(db:Annotated[Session, Depends(get_db)]):
    stmt = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)

    todos = db.execute(stmt).mappings().all()
    return {"message": "List of TODO items", "data": todos}

@router.get("/{id}")
def show(id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    return {"message": "Get a TODO item", "data": todo}

@router.post("/")
def store(item: CreateTodo, db:Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content = item.content, is_completed = item.is_completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"Message": "Create a TODO item", "item": todo}


@router.put("/{id}")
def update(id:int, item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "TODO item not found"}
    todo.content = item.content
    todo.is_completed = item.is_completed
    db.commit()
    db.refresh(todo)
    return {"message": "TODO item updated successfully", "item": todo}


@router.delete("/{id}")
def delete(id:int, db:Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "TODO item is not found"}

    db.delete(todo)
    db.commit()

    return {"message": "TODO item deleted successfully"}