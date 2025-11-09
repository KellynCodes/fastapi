
from pydantic import BaseModel


class ItemResponse(BaseModel):
    name: str
    price: float
    is_offer: bool = False
