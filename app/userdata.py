# userdata.py

from fastapi import APIRouter, HTTPException,status
from pydantic import BaseModel
import random
from typing import Optional
from .database import db
from .auth import hash_password,verify_password,get_user

identifier=0

router = APIRouter()

class User(BaseModel):
    UserName: str
    Name: str
    Password: str
    unique_id: Optional[str] = None

    # def __init__():
    #     unique_id=str(random.randrange(1000,1999))

class password(BaseModel):
    password: str

@router.post("/CreateUser",status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    try:
        if user.unique_id is None:
            user.unique_id = str(random.random())
        result = db.items.insert_one({
            "UserName": user.UserName,
            "Name": user.Name,
            "Password":  hash_password(user.Password),
            "identifyier": str(int(random.random()*100000))
        })
        return {"message": "User created successfully","data":user, "item_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add user: {str(e)}")


# @router.get("/checkpass")
# def create_user(plainpass:password):
#     return verify_password(plainpass.password,"$2b$12$iD1MY4GRMdhSNLyVJeEMyuoBarPMpljeDhoDeDFiN0QZlboJ9bffS")


@router.get("/getUser/{id}")
def returnuser(id):
    data = get_user(id=id)
    if data:
        # Convert ObjectId to string
        identifier=data["identifyier"]
        if "_id" in data:
            # data["_id"] = str(data["_id"])
            del data["_id"]
        if "Password" in data:
            del data["Password"]
        print(identifier)
        return data
    else:
        raise HTTPException(status_code=404, detail="User not found")
    