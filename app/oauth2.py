# pip install python-jose[cryptography]
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import userschemas
from fastapi import Depends, status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import usermodels

# SECRET_KEY
# Algorithm
# Expiration time
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# tokenUrl is the end point - i think login page is the end point of authentication

from .config import settings

SECRET_KEY = settings.secret_key
#  SECRET_KEY can be anything in string- we can also take "hello", so generally we take long texts
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id : str = payload.get("user_id")

        if id is None:
            return credentials_exception
        token_data = userschemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credentials_exception)

    user = db.query(usermodels.User).filter(usermodels.User.id == token.id).first()

    return user
