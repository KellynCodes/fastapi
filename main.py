from contextlib import asynccontextmanager
from fastapi import FastAPI
from data.db import metadata, engine, database
from middleware.request_time_middleware import LogRequestTime
from routes.auth_route import AuthController
from routes.product_route import ProductController

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

# ROUTES
app.include_router(AuthController().router, prefix="/auth", tags=["Auth"])
app.include_router(ProductController().router, prefix="/products", tags=['Product'])