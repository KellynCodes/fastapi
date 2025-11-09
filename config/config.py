
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Config(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")
    
    