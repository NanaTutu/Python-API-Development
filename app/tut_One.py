from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#create validation template for post data
class POST(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None    

#save posts in array
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content":"i like pizza", "id": 2}] 

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
           return p 

def find_index_post(id):
    for i ,p  in enumerate (my_posts) :
        if p['id'] == id:
            return i

# decorator
@app.get("/")

#function
async def root():
    return {"message": "welcome to my api!!!!!!!"}

# read 
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#create
@app.post("/createposts")
#extract data from post
def create_posts(payload: dict = Body(...)):
    return {"new_post": f"title: {payload['title']}, content:{payload['content']}"}

#read
@app.post("/pydantic", status_code=status.HTTP_201_CREATED)
def create_pydantic(post:POST):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data:":post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}

#delete
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update
@app.put("/posts/{id}")
def update_post(id: int, post:POST):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'message': "updated post"}
