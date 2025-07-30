from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)

db = client["taskdatabase"]
task_collection = db["tasks"]