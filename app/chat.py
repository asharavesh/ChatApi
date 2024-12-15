import json
from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from .database import db
from pydantic import BaseModel
from .auth import get_current_user_ws, TokenData
from pymongo.errors import PyMongoError
from bson import json_util

chatrouts = APIRouter()


def parse_json(data):
    return json.loads(json_util.dumps(data))


class Message(BaseModel):
    content: str
    sender: str

class userModel(BaseModel):
    UserName:str
    identifyier:str

class Chatroom(BaseModel):
    roomID: str
    messages: List[Message] = []

clients = {}
chatrooms_collection = db['ChatRooms']

async def send_updates(chatRoomID: str, websocket: WebSocket,user:userModel):
    while True:
        data = await websocket.receive_text()
        message = {"user": user.identifyier, "message": data}
        chatrooms_collection.update_one({"roomID": chatRoomID}, {"$push": {"messages": message}})
        for client in clients[chatRoomID]:
            await client.send_text(json.dumps(message))

@chatrouts.websocket("/connect/{chatRoomID}")
async def chatroom(websocket: WebSocket, chatRoomID: str, user: TokenData = Depends(get_current_user_ws)):
    await websocket.accept()
    
    if chatRoomID not in clients:
        clients[chatRoomID] = []
    clients[chatRoomID].append(websocket)
    
    chatroom = chatrooms_collection.find_one({"roomID": chatRoomID})
    if not chatroom:
        # Create a new chat room if it doesn't exist
        new_chatroom = {"roomID": chatRoomID, "messages": []}
        chatrooms_collection.insert_one(new_chatroom)
        chatroom = new_chatroom
    print(chatroom)
    await websocket.send_json(parse_json(chatroom['messages']))
    
    try:
        await send_updates(chatRoomID, websocket,user)
    except WebSocketDisconnect:
        clients[chatRoomID].remove(websocket)
        if not clients[chatRoomID]:
            del clients[chatRoomID]

# @chatrouts.websocket("/test")
# async def websocket_test(websocket: WebSocket, token: str = Depends(get_current_user_ws)):
#     await websocket.accept()
#     try:
#         while True:
#             datauser=dict(token)

#             await websocket.send_json(datauser['username'])
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message received: {data}")
#     except WebSocketDisconnect:
#         await websocket.close()
