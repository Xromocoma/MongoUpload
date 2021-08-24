from skyproto_pb import media_pb2_grpc
from src.db import MongoDBConnection
from src.upload import upload_file
from asyncio import create_task
from src.grpc import channel
from config import START_FROM, LIMIT


async def chat_rooms():
    mongo_client = MongoDBConnection().client
    mongo_db = mongo_client.chat_db
    res = mongo_db['room'].find({"room_avatar_id": {"$regex": "http"}}).skip(START_FROM).limit(START_FROM+LIMIT)
    stub_grpc = media_pb2_grpc.MediaStub(channel)

    tasks = []
    async for item in res:
        tasks.append(create_task(chat_rooms_updater(stub_grpc, item, mongo_db['room'])))

    for task in tasks:
        await task
    print('chat_room end')


async def chat_rooms_updater(stub_grpc, doc, mongo_db):
    file = await upload_file(doc['room_avatar_id'], stub_grpc)
    if file:
        temp = await mongo_db.update_one({"_id": doc['_id']}, {"$set": {"room_avatar_id": file}})
        if temp == 0:
            print("err")

