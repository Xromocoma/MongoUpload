from mongoengine import connect, disconnect_all
from config import *


class Connection:
    def __init__(self):
        connect(
            alias='src-profile',
            db='profile_db',
            host=f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&replicaSet=userReplicaSet", )

        connect(
            alias='src-event',
            db='event_db',
            host=f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&replicaSet=userReplicaSet", )

        connect(
            alias='src-chat',
            db='chat_db',
            host=f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&replicaSet=userReplicaSet", )

    def __del__(self):
        disconnect_all()
