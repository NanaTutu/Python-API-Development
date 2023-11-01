from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .router import post,users


models.Base.metadata.create_all(bind=engine)

    

# Define the cursor object outside of the try block
app = FastAPI()
# conn = None
# cursor = None

app.include_router(post.router)
app.include_router(users.router)

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts





