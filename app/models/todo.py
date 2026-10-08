from pydantic import BaseModel, Field
from typing import Optional

class CreateTodo(BaseModel):
    content: str = Field(...,max_length=500, min_length=5)
    is_completed: bool = False

