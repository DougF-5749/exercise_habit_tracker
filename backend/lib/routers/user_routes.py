import os
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Form, Depends
import lib.models.models as models
from lib.dependencies import db_dependency
from lib.schemas.user_schema import UserIn, UserBase, UserOut, Token
from typing import Annotated
from lib.security import (
    get_password_hash, 
    authenticate_user, 
    auth_dependency, 
    get_current_user,
    create_access_token,
    oauth2_req_form_dependency)

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

user_router = APIRouter(
    prefix="/users", # a URL prefix that will be applied to all routes/endpoints defined within this router
    tags=["users"] # All routes in this router will be grouped under the users tag in the automatically generated documentation
    )

# Create a new user
@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, db: db_dependency):
    # ToDO: Create crud operations for the User model and replace the query below with a call to the get_user_by_username function
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

# Fetch a logged in user --> must be placed before the fetch a user by ID route
@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user

# Fetch a user by ID
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#  Delete a user
@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(token: auth_dependency, user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# The ... is a shorthand way to tell FastAPI that a field is required. 
# It’s equivalent to setting Form(required=True)
# If the client does not provide the field in the request, FastAPI will return an error (HTTP status code 422 Unprocessable Entity
@user_router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login(db: db_dependency, form_data: oauth2_req_form_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # JWT token generation:
    access_token_expired = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, 
        expires_delta=access_token_expired
        )
    return Token(access_token=access_token, token_type="bearer")


