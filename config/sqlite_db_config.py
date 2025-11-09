from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select
from typing import Optional
from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session
from dto.item_dto import ItemResponse
from models.item_model import Item

sqlite_file_name: str = 'database.db'
sqlite_url: str = f"sqlite:///{sqlite_file_name}"

sqlite_engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(sqlite_engine)


@asynccontextmanager
async def lifespan(app: FastAPI): 
    create_db_and_tables()
    yield
    
    

app = FastAPI()

@app.post("/items", response_model= ItemResponse)
def create_item(item: Item):
    with Session(sqlite_engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.get('/items', response_model=list[Item])
def get_items():
        with Session(sqlite_engine) as session:
            items = session.exec(select(Item)).all()
            return items