from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str    
    
class ProductSchema(BaseModel):
    name: str
    description: str
    quantity: int
    price: float