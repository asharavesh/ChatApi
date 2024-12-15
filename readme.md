
# Chat Api

A Chat API (Application Programming Interface) is a backend service that provides the functionality to build chat or messaging systems within applications. It typically allows developers to integrate features like real-time messaging, group chats, file sharing, presence indicators (online/offline status), message delivery receipts, and more.



## features


* Real-time Messaging: Users can send and receive messages instantly via WebSockets.
* User Authentication: Secure login and registration system using password hashing with bcrypt.
* Message Persistence: All messages are stored in a MongoDB database for future retrieval.
* Environment Variables: Securely manage secrets and configurations via .env.
## Technologies Used

* FastAPI: For building the REST and WebSocket API.
* MongoDB: For storing users, messages, and chat groups.
* WebSockets: For real-time communication.
* bcrypt: For secure password hashing.
* python-dotenv: For loading environment variables from a .env file.
## Requirements

* Python 3.9+
* MongoDB
* FastAPI
* pip (for managing dependencies)
## Installation

1. Clone the repository:
```console
git clone https://github.com/your-username/chat-api.git
cd chat-api
```
2. Create and activate a virtual environment:
```console
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the dependencies:
```console
pip install -r requirements.txt

```
4. Set up environment variables:
```console
DBCONNECTIONSTRING=mongodb://localhost:27017
SECRET_KEY=your_secret_key
```
5. Run the application:
```console
uvicorn app.main:app --reload
```
## Endpoints

you can access all the endpoints through 
```console 
http://localhost:8000/docs
```