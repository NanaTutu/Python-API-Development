from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException,APIRouter
from pydantic import BaseModel
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()

#fetch data from database
@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#inset data into database
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db:Session = Depends(get_db)):

    # method one
    # new_post = models.Post(title = post.title, content=post.content, published=post.published)
    
    #method two
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get data by a condition
@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post

#delete data
@router.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session=Depends(get_db)):
     
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update data
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.UpdatePost, db: Session=Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query.update({'title': "my updated title", 'content': "my updated content"}, synchronize_session=False)

    db.commit()

    return post_query.first()