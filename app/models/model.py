from sqlalchemy import Column ,ForeignKey, Integer , String ,DateTime,Boolean
from app.database.db import Base

class User(Base):

    __tablename__="user_register"
    id=Column(Integer,  autoincrement=True,primary_key=True,index=True)
    username=Column(String,unique=True)
    email=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    worked_test=Column(Boolean,default=False)  #if the number of tests are increased here we can change boolean inot list of integers where we create worked tests of user we save and recheck if user worked the numbered test or not 
    point=Column(Integer,default=5)

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer, autoincrement=True,primary_key=True,index=True)
    name=Column(String)
    image1=Column(String)
    image2=Column(String)
    image3=Column(String)
    description=Column(String)
    point=Column(Integer)
    
    
class Test(Base):
    __tablename__="test"
    id=Column(Integer, autoincrement=True,primary_key=True,index=True)
    question=Column(String)
    a=Column(String)
    b=Column(String)
    c=Column(String)
    d=Column(String)
    answer=Column(String)
    