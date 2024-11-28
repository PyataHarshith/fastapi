from fastapi import APIRouter

from fastapi import Depends,HTTPException,Response,status
from sqlalchemy.orm import Session

from ..database import get_db

from ..models import postmodels
# above line creates the table in postgreSQL
from ..schemas.postschemas import post, postresponse,PostOut

from typing import List, Optional
from .. import oauth2

router = APIRouter(
    prefix = "/sqlalchemy",
    tags=["Posts"]
)

# tags is used make groups in https://...../docs page

# @router.get("/", response_model=List[postresponse])
# def get_posts(db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
#     post = db.query(postmodels.Post).filter(postmodels.Post.user_id == current_user.id).all()
#     # db.query(models.Post) - select * from Post
#     return post
#  since in above function retunred post is list of data so when we write response_model = postresponse it expects to return only data with attributes
# but to return the list of many data with their attributes we have to write response_model = List[postresponse]


# Query parameters
# https://...../sqlalchemy/?limit=3 - ? indicates to select query parameter limit
# https://...../sqlalchemy/?limit=3&skip=2 - to write another query parameter use &
# http://127.0.0.1:8000/sqlalchemy/?search=your%20post - %20 represents space

from sqlalchemy import func
# func contains functions like count and so on

# @router.get("/", response_model=List[postresponse])
@router.get("/",response_model=List[PostOut])
def get_posts(db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit: int = 10, skip : int = 0, search: Optional[str] = ""):
    # print(limit)
    # post = db.query(postmodels.Post).filter(postmodels.Post.user_id == current_user.id,postmodels.Post.title.contains(search)).limit(limit).offset(skip)
    # # whenever you want to check the python query in sql for verification just print it
    # print(post)
    # post = post.all()

    posts = db.query(postmodels.Post, func.count(postmodels.Votes.post_id).label("votes")).join(postmodels.Votes,
                        postmodels.Post.id == postmodels.Votes.post_id, isouter=True).group_by(postmodels.Post.id).filter(
                            postmodels.Post.user_id == current_user.id,postmodels.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # # whenever you want to check the python query in sql for verification just print it
    # result = query.all()
    # response = [
    #     {
    #         "post": {
    #             "id": post.id,
    #             "title": post.title,
    #             "content": post.content,
    #             "published": post.published,
    #             "user_id": post.user_id,
    #         },
    #         "votes": votes
    #     }
    #     for post, votes in result
    # ]

    # result = [
    #     {
    #         "post": post.__dict__,  # Convert SQLAlchemy model to dict
    #         "votes": votes
    #     }
    #     for post, votes in results
    # ]
    return posts


# @router.post("/",response_model=postresponse)
# def create_post(post: post,db : Session = Depends(get_db)):
#     # new_post = models.Post(title = post.title, content = post.content, published = post.published)
#     # since only three fields it is easy to type, suppose if we have 50 fields then
#     new_post = postmodels.Post(**post.dict())
#     # **post.dict() - post is converted to dictionary and then unpacked to convert it into title = post.title, content = post.content, published = post.published
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     # db.refresh - we retreive the changes committed in db and stord back into new_post
#     return new_post

@router.post("/",response_model=postresponse)
def create_post(post: post,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #  current_user : int = Depends(oauth2.get_current_user) if this is not there , then anyone can create a post in an app. so to create an app he/she must be logged in 
    # if he/she is not logged into app, then they are not allowed to create a post
    print(current_user.email)
    post = post.dict()
    post["user_id"] = current_user.id
    print(current_user.id)
    new_post = postmodels.Post(**post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=PostOut)
async def get_post(id : int, response : Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
 
    # post = db.query(postmodels.Post).filter(postmodels.Post.id == id).first()
    #  filter -- where
    post = db.query(postmodels.Post, func.count(postmodels.Votes.post_id).label("votes")).join(postmodels.Votes,
                        postmodels.Post.id == postmodels.Votes.post_id, isouter=True).group_by(postmodels.Post.id).filter(postmodels.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    return post


@router.delete("/{id}")
def delete_post(id:int, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(postmodels.Post).filter(postmodels.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    #  study what is synchronize_session through internet
    db.commit()
    return {"post": "post deleted successfully"}


@router.put("/{id}",response_model=postresponse)
def update_post(id : int, post :post,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(postmodels.Post).filter(postmodels.Post.id == id)
    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if posts.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"Updated_post" :post_query.first()}