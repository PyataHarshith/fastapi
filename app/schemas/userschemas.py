from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class usercreate(BaseModel):
    email : EmailStr
    password: str
#  Emailstr used to because whenever user enters a string that doesn't look like email it shows an error - this is not a email validation

class userinfo(BaseModel):
    id : int
    email: str
    class Config:
        orm_model = True
        # but i think we can use even without config class

class userlogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[int] = None