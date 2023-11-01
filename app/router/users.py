from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException,APIRouter
from pydantic import BaseModel
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter()

# User registeration example
@router.post('/register', response_model=schemas.RegisterResp, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.RegisterUser, db: Session=Depends(get_db)):

    #hash the password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# retrieve user information by id
@router.get("/user/{id}", response_model=schemas.FetchResp)
def get_user_by_id(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist")
    
    return user
