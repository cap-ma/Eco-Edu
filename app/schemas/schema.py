

from typing import List, Optional

from pydantic import BaseModel,EmailStr

from typing import  List

class User(BaseModel):
    username:str
    email:EmailStr

class UserCreate(User):
    password:str
  
class UserInDb(User):
    hashed_password:str
    point:int
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    username:Optional[str]=None

class Tasks(BaseModel):
    id:int
    name:int
    image1:str
    image2:str
    image3:str
    description:str
    point:int
class Test(BaseModel):
    id:int
    question:str
    a:str
    b:str
    c:str
    d:str
    answer:str

    class Config:
        orm_mode = True

class TestReturn(BaseModel):
    id:int
    question:str
    a:str
    b:str
    c:str
    d:str
    class Config:
        orm_mode = True