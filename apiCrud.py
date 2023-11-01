from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# decorator
@app.get("/")

#function
async def root():
    return {"message": "welcome to my api!!!!!!!"}