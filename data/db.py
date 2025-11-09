



from databases import Database
from sqlalchemy import Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import create_engine, MetaData

DATABASE_URL: str = "sqlite:///users.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
