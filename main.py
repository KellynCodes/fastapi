from contextlib import asynccontextmanager
from fastapi import FastAPI
from data.db import metadata, engine, database
from exceptions.exception_handler import CustomerExceptionHandler
from middleware.request_time_middleware import LogRequestTime
from routes.auth_route import AuthController
from routes.exception_route import CustomExceptionController
from routes.product_route import ProductController
from routes.template_route import TemplateController
from routes.upload_route import FileUploadController

app = FastAPI()

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()   
    
    

@app.get('/')
async def is_running():
    return {"app": "running..."} 

#MIDDLEWARES
app.add_middleware(LogRequestTime)

# EXCEPTION HANDLER
CustomerExceptionHandler().register_exception_handlers(app)

# ROUTES
app.include_router(AuthController().router, prefix="/auth", tags=["Auth"])
app.include_router(ProductController().router, prefix="/products", tags=['Product'])
app.include_router(TemplateController().router, prefix="/templates", tags=['Templates'])
app.include_router(CustomExceptionController().router, prefix="/exceptions", tags=['Exceptions'])
app.include_router(FileUploadController(app).router, prefix="/uploads", tags=['Uploads'])