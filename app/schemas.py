from pydantic import BaseModel, EmailStr

#create validation template for post data
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


#schema for inserting user
class RegisterUser(BaseModel):
    email: EmailStr
    password: str     
    
#Registeration response schema
class UserBase(BaseModel):
    id: int
    email: EmailStr

# registeration response schema
class RegisterResp(UserBase):
    pass

    class Config:
        orm_mode = True

#fetch schema
class FetchResp(UserBase):
    pass       

# class POST(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True    