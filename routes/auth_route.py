from fastapi import APIRouter, HTTPException
from schemas.schema import UserCreate, UserLogin
from models.models import Users
from data.db import database
from security.bcrypt import Bcrypt
from services.auth_service import AuthService


class AuthController:
    router: APIRouter  = APIRouter()
    authService: AuthService = AuthService()
    
    def __init__(self):
        self.router.post("/register")(self.register)
        self.router.post("/login")(self.login)
         
    
    async def register(self, user: UserCreate):
       return await self.authService.signup(user)

    async def login(self, user: UserLogin):
        return await self.authService.login(user)