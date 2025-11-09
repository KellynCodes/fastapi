
from typing import Optional
from sqlmodel import Field, SQLModel


class Item(SQLModel, table = True): 
    id: Optional[int] = Field(default = None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False
    