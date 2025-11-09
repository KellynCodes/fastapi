from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from sqlalchemy import Engine
from sqlmodel import Field, SQLModel, create_engine
from fastapi import FastAPI
from sqlmodel import Session, select
from dto.item_dto import ItemResponse
from models.item_model import Item


db_url: str = 'postgresql+psycopg2://postgres:123456789@localhost:5432/FastAPI'
postgres_engine: Engine = create_engine(db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(postgres_engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
    
    
app: FastAPI = FastAPI(lifespan=lifespan)

@app.post("/items", response_model= ItemResponse)
def create_item(item: Item):
    with Session(postgres_engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.get('/items', response_model=list[Item])
def get_items():
        with Session(postgres_engine) as session:
            items = session.exec(select(Item)).all()
            return items    