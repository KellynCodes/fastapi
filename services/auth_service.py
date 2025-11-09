from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import Select
from config.config import Config
from jose import JWSError, jwt
from databases.core import Record
from sqlalchemy import Insert, Select
from schemas.schema import UserCreate, UserLogin
from models.models import  Users
from security.bcrypt import Bcrypt
from data.db import database
from exceptions.exception_handler import UnauthorizedException


class AuthService:
    config = Config()
    security = HTTPBearer()
    
    async def signup(self, user: UserCreate) -> UserCreate | dict:
       """Sign up new user"""
       try:
            user_exist_query: Select[any] = Users.select().where(Users.c.username == user.username)
            existing_user: Record | None = await database.fetch_one(user_exist_query)
            if existing_user:
                return {"status_code": 400, "message": "User already exists"}
            
            hashed_password: str = Bcrypt().hash(user.password)
            insert_query: Insert = Users.insert().values(username=user.username, password=hashed_password)
            await database.execute(insert_query) 
            return {"message": "User created successfully"}
       except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail= "Sorry we are unable to create your account. Please try again or contact support.")

       
    async def login(self, user: UserLogin) -> dict:
        """Login existing user"""
        user_exist_query: Select[any] = Users.select().where(Users.c.username == user.username)
        db_user: Record | None = await database.fetch_one(user_exist_query)  
        if not db_user or not Bcrypt().verify(user.password, db_user['password']):
            raise UnauthorizedException(message="Invalid credentials")
        
        access_token: str = self.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer", "user": db_user}
        
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
       """
       Create a new access token.
       """
       encode: dict = data.copy()
       expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=self.config.access_token_expires_in_minutes))
       encode.update({"exp": expire})
       jwt_token: str = jwt.encode(encode, self.config.secret_key, algorithm=self.config.algorithm)
       return jwt_token
       
    def verify_token(self, token: str) -> bool:
       """
       Verify the provided JWT token.
       """
       try:
           payload = jwt.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
           return True
       except JWSError as e:
           print(f"Token verification failed: {e}")
           return False
    
    