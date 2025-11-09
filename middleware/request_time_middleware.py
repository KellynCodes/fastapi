import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class LogRequestTime(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next): 
        start_time = time.time()
        process_time: float = time.time() - start_time
        print(f"Request: {request.method} {request.url} - Process time: {process_time:.4f} seconds")
        return await call_next(request)