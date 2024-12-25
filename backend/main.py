from fastapi import FastAPI

from lib.database import engine
from lib.routers.user_routes import user_router
from lib.database import Base

app = FastAPI()

# create tables in database
Base.metadata.create_all(bind=engine)

# Routes: Abstract to routes folder/files and import into main.py
app.include_router(user_router)

@app.get("/")
async def index():
    return {"message": "Hello World"}
