from fastapi import APIRouter, HTTPException, status, Form
import lib.models.models as models
from lib.dependencies import db_dependency
from lib.schemas.user_schema import UserIn, UserBase, UserOut
from lib.schemas.user_schema import LoginFormData
from lib.security import get_password_hash, authenticate_user

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

# Fetch a user by ID
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Fetch a logged in user
@user_router.get("/my_profile", status_code=status.HTTP_200_OK, response_model=UserBase)
# async def get_user(user_id: int, db: db_dependency):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

#  Delete a user
@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

@user_router.post("/token")
async def login(data: LoginFormData = Form(...)):
    return data
# The ... is a shorthand way to tell FastAPI that a field is required. 
# It’s equivalent to setting Form(required=True)
# If the client does not provide the field in the request, FastAPI will return an error (HTTP status code 422 Unprocessable Entity
