from config import *
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBConnection:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&replicaSet=userReplicaSet", )

    def __del__(self):
        self.client.close()
