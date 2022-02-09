from datetime import datetime, timedelta
from email.mime import image
from operator import truediv
from typing import Optional
import os


from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from database.db import SessionLocal
from models import model
from schemas import schema
from database import db 
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import sqlalchemy

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv(r"C:\repositories\Eco-Edu_github\Eco-Edu\Eco-Edu\app\.env")
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM=os.environ.get("ALGORITHM")
password_r=os.environ.get("PASSWORD")



app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(model.User).filter(model.User.username==username).first()

def create_user(db:Session,user:schema.UserCreate):
    
    db_user=model.User(username=user.username,hashed_password=get_password_hash(user.password),email=user.email,worked_test=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db:Session, username: str, password: str):
    user = get_user(db, username)
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#############3TASK########333
def create_tasks(db:Session,name:str,description:str,image1:str,image2:str,image3:str,point:int):
    db_task=model.Task(name=name,description=description,image1=image1,image2=image2,image3=image3,point=point)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

def get_tasks_image1_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.image1

def get_tasks_image2_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.image2

def get_tasks_image3_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.image3

def get_tasks_name_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.name

def get_tasks_description_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.description

def get_tasks_point_logic(db:Session,id:int):
    task_obj=db.query(model.Task).filter(model.Task.id==id).first()
    return task_obj.point
def get_question_logic(db:Session):
    test=db.query(model.Test).all()
    return test
#####################TEST#######################

def post_test_logic(db:Session,password:int,test:schema.Test):
    if password==int(password_r):
        obj=model.Test(question=test.question,a=test.a,b=test.b,c=test.c,d=test.d,answer=test.answer)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    else :

        return password+"you are not admin" 

def get_all_test(db:Session):
    obj=db.query(model.Test).all()
    return obj
    
def post_test(db:Session,id:int,answer:str):
    real_answer=db.query(model.Test).filter(model.Test.id==id).first()
    if real_answer.answer==answer:
        return True
    else:
        return False

        
def change_user_worked_test_into_true(db:Session,username:str):
    user=db.query(model.User).filter(model.User.username==username).first()
    user.worked_test=True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def change_user_point(db:Session,username:str):
    user_point_change=db.query(model.User).filter(model.User.username==username).first()
    user_point_change.point+3
    db.add(user_point_change)
    db.commit()
    db.refresh(user_point_change)
    return user_point_change