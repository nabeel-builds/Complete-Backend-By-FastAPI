from fastapi import APIRouter
from app.models.todo import CreateTodo

router = APIRouter(
    prefix="/todo"
)

@router.get("/")
def index():
    return {"Message": "This is todo router"}

@router.post("/")
def store(item:CreateTodo):
    return {"Message": "Create a TODO item", "item": item.model_dump()}