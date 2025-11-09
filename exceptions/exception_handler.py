from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 404
        
class UnauthorizedException(Exception):
    def __init__(self, message: str): 
        self.message = message
        self.status_code = 401
        
class BadRequestException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 400
        
class InternalServerErrorException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 500

class CustomerExceptionHandler:
    def register_exception_handlers(self, app: FastAPI):
        app.add_exception_handler(NotFoundException, self.not_found_exception_handler)
        app.add_exception_handler(UnauthorizedException, self.unauthorized_exception_handler)
        app.add_exception_handler(BadRequestException, self.bad_request_exception_handler)
        app.add_exception_handler(InternalServerErrorException, self.internal_server_error_exception_handler)
    
    async def not_found_exception_handler(self, request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )

    async def unauthorized_exception_handler(self, request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )

    async def bad_request_exception_handler(self, request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )

    async def internal_server_error_exception_handler(self, request: Request, exc: InternalServerErrorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )   