import bcrypt
from bson import json_util
from .database import db
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException,status,Depends,Body,WebSocket
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

authRoute=APIRouter()

SECRET_KEY = os.getenv("SECRETKEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: Optional[str] = None
    identifyier: Optional[str]=None



def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    return hashed_password_str

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_user(id: str):
    try:
        userdoc = db.items.find_one({"identifyier": id})
        if userdoc:
            # Convert MongoDB document to JSON serializable format
            userdoc = json_util.dumps(userdoc)
            return json_util.loads(userdoc)
        else:
            return None
    except Exception as e:
        print(f"Could not find the user or an error occurred: {e}")
        return None


def get_user_for_auth(UserName):
    try:
        userdoc = db.items.find_one({"UserName": UserName})
        if userdoc:
            # Convert MongoDB document to JSON serializable format
            userdoc = json_util.dumps(userdoc)
            return json_util.loads(userdoc)
        else:
            return None
    except Exception as e:
        print(f"Could not find the user or an error occurred: {e}")
        return None
    
    
def check_user(user,password)->bool:
    Userdoc=get_user_for_auth(UserName=user)
    if not Userdoc:
        return False
    if not verify_password(password,Userdoc["Password"]):
        return False
    if "_id" in Userdoc:
        del Userdoc["_id"]
    return Userdoc

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def Get_current_user(token: str=Depends(oauth2_scheme) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("UserName")
        if username is None:
            raise credentials_exception
    
        token_data = TokenData(username=username,identifyier=payload.get("identifyier"))
    except JWTError:
        raise credentials_exception
    user = {"Usename":token_data.username,"identifyier":token_data.identifyier}
    print(user)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_ws(websocket: WebSocket, token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("UserName")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username,identifyier=payload.get("identifyier"))
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise credentials_exception
    return token_data



@authRoute.get("/login/{Username}/{Password}")
def login(Username,Password):
    userData = check_user(Username,Password)
    if not userData:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=userData, expires_delta=access_token_expires
    )
    return {"access_token":access_token,"token-type":"bearer"}
    
    # return Get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyTmFtZSI6ImpvaG5fZG9lMSIsIk5hbWUiOiJKb2huIERvZSIsIlBhc3N3b3JkIjoiJDJiJDEyJGlEMU1ZNEdSTWRoU05MeVZKZUVNeXVvQmFyUE1wbGplRGhvRGVERmlOMFFabGJvSjliZmZTIiwiaWRlbnRpZnlpZXIiOiIxNTUzOCIsImV4cCI6MTcyMDgxMTYyNX0.G636CwlsXxrGxf_zaJDYVCaZfgwddLjNbOKatSscQHw")


@authRoute.get('/checkauth')
def checkauth(user:TokenData=Depends(Get_current_user)):
    print(f"{user}")
    return "login test"
