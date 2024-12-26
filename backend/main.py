from fastapi import FastAPI, Form

from lib.database import engine
from lib.routers.user_routes import user_router
from lib.database import Base
from lib.schemas.user_schema import LoginFormData

app = FastAPI()

# create tables in database
Base.metadata.create_all(bind=engine)

# Routes: Abstract to routes folder/files and import into main.py
app.include_router(user_router)

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.post("/login")
async def login(data: LoginFormData = Form(...)):
    return data
# The ... is a shorthand way to tell FastAPI that a field is required. 
# It’s equivalent to setting Form(required=True)
# If the client does not provide the field in the request, FastAPI will return an error (HTTP status code 422 Unprocessable Entity
