# main.py

from fastapi import FastAPI
from .userdata import router
from .auth import authRoute  # Import your router from userdata.py
from .chat import chatrouts
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Include the router using app.include_router()
app.include_router(router)
app.include_router(authRoute,prefix="/auth")
app.include_router(chatrouts,prefix='/chat')

@app.get("/")
def home():
    # print(os.getenv("DBCONNECTIONSTRING"))
    return {"message": "Welcome to the main page"}


@app.get("/auttest")
def testauth():
    return {"status":"token verified"}