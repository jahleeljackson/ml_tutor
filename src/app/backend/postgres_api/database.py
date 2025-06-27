from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
import os 
from dotenv import load_dotenv

load_dotenv()
postgres_uri = "postgresql://postgres:9305*Elcon@db:5432/ml_tutor" #use os.getenv('POSTGRES_URI') not running with docker



SQLALCHEMY_DATABASE_URL = postgres_uri


#creating engine to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure the session is closed after use
        


