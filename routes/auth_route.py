from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from jose import JWSError
from schemas.schema import UserCreate, UserLogin
from services.auth_service import AuthService


class AuthController:
    router: APIRouter  = APIRouter()
    authService: AuthService = AuthService()
    
    def __init__(self):
        self.router.post("/register")(self.register)
        self.router.post("/login")(self.login)
        self.router.get("/protected")(self.protected_route)
         
    
    async def register(self, user: UserCreate):
       return await self.authService.signup(user)

    async def login(self, user: UserLogin):
        return await self.authService.login(user)
    
    async def protected_route(self, token: str = Depends(AuthService.security)):
        try:
            AuthService().verify_token(token.credentials)
            return {"message": "Access granted to protected route"}
        except JWSError:
            raise HTTPException(status_code=401, detail="Invalid token")