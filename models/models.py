


from sqlalchemy import Column, Float,Integer, MetaData, Table, String
from data.db import metadata
from data.db import Base

users: Table = Table(
    "users",
    metadata,
   Column("id", Integer, primary_key=True),
    Column('username', String(50), unique=True, nullable=False, index=True),
    Column('password', String(1000))
)


class Product(Base):
    __tablename__ = "Products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=False, index=True)
    description = Column(String(200))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)