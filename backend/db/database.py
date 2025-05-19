import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

client = MongoClient(
    os.getenv('MONGO_URI'),
    tlsCAFile=certifi.where()
)

db = client[os.getenv('DB_NAME')]
