from fastapi import FastAPI, Depends
from typing import Annotated
from type import QueryParams
from app.routes import todo
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# include all routes here
app.include_router(todo.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {}
    for error in exc.errors():
        print(f"The Error is: {error}")
        errors[error["loc"][-1]] = error["msg"]

    request JSONResponse(
        {"message": "Validation Error", "errors": errors}, status_code=422
    )

@app.get("/")
def root(query: Annotated[QueryParams, Depends()]):
    return {"Message":"Hello World", "params": query}

