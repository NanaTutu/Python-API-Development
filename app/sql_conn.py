from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Define the cursor object outside of the try block
app = FastAPI()
# conn = None
# cursor = None

#create validation template for post data
class POST(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None   

# Postgres Database Connection
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break  
    except Exception as error:
        print("Connection to database failed")  
        print("Error: ", error) 
        time.sleep(5)          

# #save posts in array
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content":"i like pizza", "id": 2}] 

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
           return p 

def find_index_post(id):
    for i ,p  in enumerate (my_posts) :
        if p['id'] == id:
            return i

# # decorator
# @app.get("/")

# #function
# async def root():
#     return {"message": "welcome to my api!!!!!!!"}

# fetch information from database
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# #create a new post (insert)
@app.post("/pydantic", status_code=status.HTTP_201_CREATED)
def create_pydantic(post:POST):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data:": new_post}

# get a post with a condition 
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail":  post}

#delete
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update
@app.put("/posts/{id}")
def update_post(id: int, post:POST):
    cursor.execute(""" UPDATE posts SET title = %s, content= %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit();

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    
    return {'message': "updated post"}


   

