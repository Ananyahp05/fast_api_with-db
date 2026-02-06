from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base() 

DATABASE_URL = "sqlite:///./test.db"

def get_db():
    db = create_engine(DATABASE_URL)
    try:
        yield db
    finally:
        db.close()