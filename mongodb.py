from pymongo import MongoClient

MongoClient = MongoClient("mongodb://localhost:27017/")

try:
    MongoClient.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = MongoClient.taskz_db

    task_collection = db.tasks
    user_collection = db.users
except Exception as e:
    print(e)