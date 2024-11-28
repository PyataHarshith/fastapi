
from fastapi import Depends,HTTPException,Response,status
from sqlalchemy.orm import Session

from fastapi import APIRouter

from ..models import postmodels
from ..database import  get_db 
from ..schemas import postschemas
from .. import database, oauth2 


router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: postschemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(postmodels.Post).filter(postmodels.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} doesn't exisit")

    vote_query = db.query(postmodels.Votes).filter(postmodels.Votes.post_id == vote.post_id, postmodels.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        row = postmodels.Votes(user_id = current_user.id, post_id = vote.post_id)
        db.add(row)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully removed vote"}
