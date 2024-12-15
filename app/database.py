from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a MongoClient instance
client = MongoClient(os.getenv("DBCONNECTIONSTRING"))

# Access the 'test2' database
db = client["test2"]

# You can add further operations here, like checking a collection
print(f"Connected to database: {db.name}")
