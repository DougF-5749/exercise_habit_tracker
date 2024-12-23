from datetime import datetime
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
import lib.models as models
from lib.database import engine, SessionLocal
from sqlalchemy.orm import Session
from lib.routers.user_routes import user_router

app = FastAPI()

# create tables in database
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    date_created: datetime

class GameSessionBase(BaseModel):
    date_created: datetime
    recorded_by: int

# database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Routes: Abstract to routes folder/files and import into main.py
app.include_router(user_router)

@app.get("/")
async def index():
    return {"message": "Hello World"}
