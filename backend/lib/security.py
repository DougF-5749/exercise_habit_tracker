from passlib.context import CryptContext
from lib.dependencies import db_dependency
from lib.models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    db = db_dependency()
    # Todo: Fix this by adding a try except block to catch the error and return False
    # ToDo: Create CRUD operations for the User model and replace the query below with a call to the get_user_by_username function
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user



