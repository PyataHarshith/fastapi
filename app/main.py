from fastapi import FastAPI
# from fastapi import Depends,HTTPException,Response,status
# from sqlalchemy.orm import Session
from .routers import post, user, auth,vote
from .config import settings

from .models import postmodels
from .database import engine,Base

# Base.metadata.create_all(bind = engine)
# above line is used for sqlalchemy not for alembic


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
# used to allow other servers or computers
# CORSMiddleware - it something which runs before all requests

origins = [
    # now we can send requests through above links page
    # Example: Allow requests from a frontend running locally
    "*", 
    #  * every one
]

# fetch('http://localhost:8000/').then(res=>res.json()).then(console.log)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    # above line makesure to allow only methods(get,post,...) to mentioned server or computer
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}
