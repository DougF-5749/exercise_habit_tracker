from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from lib.database import SessionLocal

def get_db():
    """Database session generator for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
