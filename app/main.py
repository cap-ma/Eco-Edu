import asyncio
from fastapi import FastAPI, Form, Cookie, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
from datetime import datetime, timedelta
from typing import Optional
from database import db as datahub
from logics import logic
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models import model
from schemas import schema
from dotenv import load_dotenv
import os 
import config 

from sqlalchemy.orm import Session

settings = config.Settings()

app = FastAPI()
client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

load_dotenv("C:\repositories\Eco-Edu_github\Eco-Edu\app\.env")
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM=os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES_STR=os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES=int(ACCESS_TOKEN_EXPIRE_MINUTES_STR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db=datahub.SessionLocal()
    try:
        yield db
    finally:
       db.close()



def send_verification_code(email):
    verification = client.verify.services(
        settings.twilio_verify_service).verifications.create(
            to=email, channel='email')
    assert verification.status == 'pending'

@app.get('/')
async def index():
    return FileResponse('index.html')

@app.post('/')
async def handle_form(email: str = Form(...)):
       await asyncio.get_event_loop().run_in_executor(
        None, send_verification_code, email)
       response = RedirectResponse('/verify',
                                status_code=status.HTTP_303_SEE_OTHER)
       response.set_cookie('email', email)
       return response


@app.get('/verify')
async def verify():
    return FileResponse('verify.html')

def check_verification_code(email, code):
    verification = client.verify.services(
        settings.twilio_verify_service).verification_checks.create(
            to=email, code=code)
    return verification.status == 'approved'

@app.post('/verify')
async def verify_code(email: str = Cookie(None), code: str = Form(...)):
    verified = await asyncio.get_event_loop().run_in_executor(
        None, check_verification_code, email, code)
    if verified:
        return RedirectResponse('/success',
                                status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/verify',
                                status_code=status.HTTP_303_SEE_OTHER)
@app.get('/success')
async def success():
    return FileResponse('success.html')


def get_current_user(db:Session=Depends(get_db) ,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data=username
    except JWTError:
        raise credentials_exception
    user = logic.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user




@app.post("/token", response_model=schema.Token)
async def login_for_access_token(db:Session=Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = logic.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = logic.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create_user")
async def user_create(user:schema.UserCreate,db:Session=Depends(get_db)):
    userInDb=logic.get_user(db=db,username=user.username)
    if userInDb:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user with this username is already registered",
            
        )

    return logic.create_user(user=user,db=db)


