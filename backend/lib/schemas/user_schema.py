from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    date_created: datetime

# Note: UserIn is used to create a new user
# Note: UserIn inherits from UserBase
class UserIn(UserBase):
    password: str