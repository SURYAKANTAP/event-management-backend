import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# THE FIX IS HERE: Add connect_args with pool options
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,  # Number of connections to keep open in the pool
    max_overflow=2, # Number of extra connections to allow
    pool_recycle=300, # Recycle connections every 300 seconds (5 minutes)
    pool_pre_ping=True, # Check connection health before use
    pool_use_lifo=True, # Use Last-In, First-Out for connection retrieval
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()