from re import A
from fastapi import FastAPI, Form, Cookie, status,Depends,UploadFile,File
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
from datetime import datetime, timedelta
from typing import Optional
from app.database import db as datahub
from app.logics import logic
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.schemas import schema
from dotenv import load_dotenv
import os 

import shutil
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


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



"""def send_verification_code(email):
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
"""

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

##########Task########################
@app.post("/tasks")
def post_tasks(name:str,description:str,point:int,image1:UploadFile=File(...),image2:UploadFile=File(...),image3:UploadFile=File(...),db:Session=Depends(get_db)):
    with open("tasks/"+image1.filename,"wb") as image1_:
        shutil.copyfileobj(image1.file,image1_)
    url1=str("tasks/"+image1.filename)  

    with open("tasks/"+image2.filename,"wb") as image2_:
        shutil.copyfileobj(image2.file,image2_)
    url2=str("tasks/"+image2.filename)  


    with open("tasks/"+image3.filename,"wb") as image3_:
        shutil.copyfileobj(image3.file,image3_)
    url3=str("tasks/"+image3.filename)  

    return  logic.create_tasks(db=db,name=name,description=description,image1=url1,image2=url2,image3=url3,point=point)


@app.get("/tasks/image1/{id}")
def get_tasks_image1(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_image1_logic(db=db,id=id)
    return FileResponse(a,media_type="image/jpg")

@app.get("/tasks/image2/{id}")
def get_tasks_image2(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_image2_logic(db=db,id=id)
    return FileResponse(a,media_type="image/jpg")

@app.get("/tasks/image3/{id}")
def get_tasks_image3(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_image3_logic(db=db,id=id)
    return FileResponse(a,media_type="image/jpg")

@app.get("/tasks/name/{id}")
def get_tasks_name(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_name_logic(db=db,id=id)
    return a

@app.get("/tasks/description/{id}")
def get_tasks_description(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_description_logic(db=db,id=id)
    return a

@app.get("/tasks/point/{id}")
def get_tasks_point(id:int,db:Session=Depends(get_db)):
    a=logic.get_tasks_point_logic(db=db,id=id)
    return a
##########################TEST###############33
@app.get("/test",response_model=schema.TestReturn)
def get_test(db:Session=Depends(get_db)):
    a=logic.get_all_test(db=db)
    json_compatible_item_data = jsonable_encoder(a)
    return JSONResponse(content=json_compatible_item_data)
    

@app.post("/test")
def get_test(test:schema.Test,password:int,db:Session=Depends(get_db)):
    a=logic.post_test_logic(db=db,password=password,test=test)
    return a

@app.put("/make_user_worked_test")
def change_user_worked_test(db:Session=Depends(get_db),user=Depends(get_current_user)):
    foo=logic.change_user_worked_test_into_true(db,user.username)
    return foo
@app.post("/work_test")
def try_work_test(answer:str,id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):#id is  which number of test user is working
    answer_counter=0
    if user.worked_test==True:
        return "you are not allowed to work test because you are already worked this test"
    else:
        answer_real=logic.post_test(db=db,id=id,answer=answer)
        for a in range(10):
            if answer_real==True:
                answer_counter=answer_counter+1
            else :
                answer_counter
        if answer_counter>=7:
            return logic.change_user_point(db=db,username=user.username)
        else :
            return "you are not worked over 7"



            

############CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#############