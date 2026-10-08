from pydantic import BaseModel
from typing import Optional

class QueryParams(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    