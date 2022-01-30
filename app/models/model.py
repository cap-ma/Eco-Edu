from datetime import datetime
from pickle import TRUE
from typing import List

from sqlalchemy import Column ,ForeignKey, Integer , String ,DateTime,Boolean
from database.db import Base

class User(Base):

    __tablename__="user_register"
   

    id=Column(Integer,  autoincrement=True,primary_key=True,index=True)
    username=Column(String,unique=True)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    