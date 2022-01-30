from datetime import datetime, timedelta
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

load_dotenv(r"C:\repositories\Eco-Edu_github\Eco-Edu\app\.env")
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM=os.environ.get("ALGORITHM")



app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(model.User).filter(model.User.username==username).first()

def create_user(db:Session,user:schema.UserCreate):
    
    db_user=model.User(username=user.username,hashed_password=get_password_hash(user.password))
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

