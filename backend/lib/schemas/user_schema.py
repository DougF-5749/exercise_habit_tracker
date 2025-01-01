from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    date_created: datetime | None = None
    # profile_picture: str | None = None

# Note: UserIn is used to create a new user
# Note: UserIn inherits from UserBase
class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class LoginFormData(BaseModel):
    username: str
    password: str
    # restrict the form fields to only those declared in the Pydantic model
    model_config = {'extra': 'forbid'}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None