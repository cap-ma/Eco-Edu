from typing import List, Optional
from urllib.request import BaseHandler
from pydantic import BaseModel
from typing import  List

class User(BaseModel):
    username:str
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