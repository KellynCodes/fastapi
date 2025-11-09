from fastapi import APIRouter, HTTPException
from sqlalchemy import Insert, Select
from schemas.schema import UserCreate, UserLogin
from models.models import users
from databases.core import Record
from data.db import database
from security.bcrypt import Bcrypt


class AuthController:
    router: APIRouter  = APIRouter()
    
    def __init__(self):
        self.router.post("/register")(self.register)
        self.router.post("/login")(self.login)
         
    
    async def register(self, user: UserCreate):
        try:
            user_exist_query: Select[any] = users.select().where(users.c.username == user.username)
            existing_user: Record | None = await database.fetch_one(user_exist_query)
            if existing_user:
                raise HTTPException(status_code=400, detail= "User alrerady exists")
            
            hashed_password: str = Bcrypt().hash(user.password)
            insert_query: Insert = users.insert().values(username=user.username, password=hashed_password)
            await database.execute(insert_query) 
            return {"message": "User created successfully"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail= "Sorry we are unable to create your account. Please try again or contact support.")


    async def login(self, user: UserLogin):
        user_exist_query = users.select().where(users.c.username == user.username)
        existing_user = await database.fetch_one(user_exist_query)
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not Bcrypt().verify(user.password, existing_user['password']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {"message": "Login successful"}