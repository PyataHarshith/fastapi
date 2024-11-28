
from pydantic import BaseModel
# pydantic guide: pydantic website
from .userschemas import userinfo
from typing import Optional
from pydantic import conint

class post(BaseModel):
    title: str
    content: str
    published : bool = True 

class create_post(post):
    pass 

class postresponse(BaseModel):
    title: str
    content: str
    published : bool
    id: int
    user_id : int
    owner : userinfo
    class Config:
        orm_model = True

# whenever we give the above class model as response model in @app.post/get/put("",response_model = ---) then we can able to show just the columns mentioned in the response model
# eg: in response model - title, content, published, so when we return post , id will not gonna appear in the userinterface or postman api check ouput 

class PostOut(BaseModel):
    Post : postresponse
    votes: int
    class config:
        orm_model = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    # no error, le=1 means value <=1
    # we get user_id from login credentials