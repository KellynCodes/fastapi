

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from exceptions.exception_handler import NotFoundException


class CustomExceptionController:
    def __init__(self):
        self.router = APIRouter()
        self.router.get("/divide")(self.divide)
        self.router.get("/not-found")(self.not_found_error)

    async def divide(self, a: float, b: float):
        try:
            result = a / b
            return {"result": result}
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
   
    async def not_found_error(self, id: int): 
        raise NotFoundException(f"Product with {id} was not found")