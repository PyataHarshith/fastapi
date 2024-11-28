
from fastapi import Depends,HTTPException,Response,status
from sqlalchemy.orm import Session

from fastapi import APIRouter

from ..models import usermodels
from ..database import  get_db  
#  . - import from present dirctory
# .. import from upper directory 

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# prefix = "/users" - so that it fixes the directory of link for below path operations

from ..schemas.userschemas import userinfo, usercreate
from ..utils import hash

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=userinfo)
def create_user(user : usercreate, db : Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = usermodels.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=userinfo)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(usermodels.User).filter(usermodels.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")
    return user