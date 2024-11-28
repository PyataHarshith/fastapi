from fastapi import APIRouter, Depends, HTTPException,status, Response
from sqlalchemy.orm import Session

from .. import database, oauth2
from ..schemas import userschemas
from ..models import usermodels
from .. import utils

router = APIRouter(tags=['Authentication'])

# @router.post("/login")
# def login(user_credentials:userschemas.userlogin, db : Session = Depends(database.get_db)):
#     user = db.query(usermodels.User).filter(usermodels.User.email == user_credentials.email).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")
    
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")

#     #  create token
#     # return token
#     access_token = oauth.create_access_token(data={"user_id": user.id})

#     return {"Access_token": access_token, "token_type": "bearer"}
#  that access oken is reffered as bearer token
#  we get access_token as eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0NywiZXhwIjoxNzMyNjczNDU1fQ.OjThGpbjE8lrtkkSGAxGIKiN9aqbRz7AUsdR-fiLksw
# to encode this token, open jwt website and paste it in encoded box we get details under decoded boxes

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

@router.post("/login", response_model=userschemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    # user_credentials - {
    #                     "username" :
    #                     "password":
    #                     }
    #  above dictionary order is from OAuth2PasswordRequestForm class/library
    user = db.query(usermodels.User).filter(usermodels.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials")

    #  create token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
#  since we used response_model, so while we return "access_token" should of same spelling in the model and also apllied to others

