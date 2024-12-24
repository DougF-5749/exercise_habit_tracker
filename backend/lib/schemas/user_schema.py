from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    date_created: datetime