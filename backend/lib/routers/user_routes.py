from fastapi import APIRouter, HTTPException, status
import lib.models.models as models
from lib.dependencies import db_dependency
from lib.schemas.user_schema import UserBase


user_router = APIRouter(
    prefix="/users", # a URL prefix that will be applied to all routes/endpoints defined within this router
    tags=["users"] # All routes in this router will be grouped under the “items” tag in the automatically generated documentation
    )

# Create a new user
@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

# Fetch a user by ID
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Fetch a loggerd in user
@user_router.get("/my_profile", status_code=status.HTTP_200_OK)
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
