from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

#  fastapi guide : fastapi website


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}

#  above three lines is a path operation
# instead of async def we can write def and can have name other than root
# @app.get("/") is a decorator without this root is just a function won't become a path operation
# @app.get("/") - get is one of the http  methods and ("/") - means root path or first page

# to  run it in the web server type following in the terminal - uvicorn <file name>: <fastapi object name> ; here it is uvicorn main: app
# if only uvicorn main: app ,then whenever we make changes, those changes won't be able to appear on web directly, so we have to break the present server and run that uvicorn main:app again
# to overcome above problem use uvicorn main:app --reload  - this automatically break server and run whenever changes are made

# if main.py is present in the folder where fastapi venv present then we can use uvicorn main:app --reload
# if we create a folder name app in the folder where fastapi venv and if main.py present in it then use uvicorn app.main:app --reload


@app.get("/posts")
async def get_posts():
    return {"Post": "This is your post"}

# if two decorators have same path(url in ("/...")) then the first decorators function will be shown 

# http method:
# 1. get : only request is sent to the api
# 2. post: we send the request and data to the api server

@app.post("/createposts")
def createposts(payload : dict = Body(...)):
    print(payload)
    # payload is a variable which stores the data given by user -if user wants to run this createposts page he must give the required data
    return {"new_post   " : f"title : {payload["title"]} content : {payload['content']}"}

#  pydantic helps to create a schema

from ..schemas.postschemas import post

# @app.post("/posts")
# def createposts(new_post : post):
#     print(new_post)
#     # new_post.title, mnew-post.content and so on
#     print(new_post.dict())
#     # new_post.dict() converts the pydantic model into a dictionary
#     # payload is a variable which stores the data given by user -if user wants to run this createposts page he must give the required data
#     return {"new_post" : new_post}

#  CRUD Operations
# 1. Create - Http method used is - post
# 2. Read - Http method used is - get - 1. for page with particular id (dynamic) - eg: posts/{id}
#                                       2. just for page
# 3. Update - Http method used is - put/patch - for page with particular id - put to update entire field and patch to update part of a field
# 4. Delete - Http method used is - delete - for page with particular page

my_posts = [{"title" : "title of post 1", "content" : "content of post 1","id" :1}, {"title": "favorite food", "content":"I like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts")
async def get_posts():
    return {"Post": my_posts}

from random import randrange
from fastapi import status

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# when ever we create something , it is best to use 201 - it signifies that "created"
async def createpost(new_post : post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post": post}

# if above three lines are written after below path we get error because if written after below path when you browse for /posts/latest it firsts checks the posts/{id} because it comes first in order so latest is passed as id 
# so order is very important in fastapi

from fastapi import Response, status, HTTPException

@app.get("/posts/{id}")
async def get_post(id : int,response : Response):
    # print(id) 
    #  the id we get will be in the form of string
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} was not found"}
    # if the post is null(data of given id is not present) we are gettng the response as ok
    # but to show the error of any type(404,502,...) we use above lines
    # status is class which contains the error types with their meanings
    return {"data" : post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# when ever we delete response code should be of 204 - because 204 signifies the deletion in http successful responses
def delete_post(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # we can't return message when we use 204 code in app.delete ---?--

# Update Operation
# 1. Put
@app.put("/posts/{id}")
def update_post(id : int, post : post):
    # print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

# http://127.0.0.1:8000/docs will give us a page that shows the order of our path operations
# similarly, http://127.0.0.1:8000/redoc

