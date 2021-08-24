from skyproto_pb import media_pb2_grpc
from src.db import MongoDBConnection
from src.upload import upload_file
from asyncio import create_task
from src.grpc import channel
from config import START_FROM, LIMIT


async def greetings():
    mongo_client = MongoDBConnection().client
    mongo_db = mongo_client.prodile_db
    res = mongo_db['greeting'].find({"greeting_avatar_id": {"$regex": "http"}}).skip(START_FROM).limit(START_FROM+LIMIT)
    stub_grpc = media_pb2_grpc.MediaStub(channel)

    tasks = []
    async for item in res:
        #tasks.append(create_task(greeting_updater(stub_grpc, item, mongo_db['greeting'])))
        await greeting_updater(stub_grpc, item, mongo_db['greeting'])
    #for task in tasks:
    #    await task
    print('greetings end')


async def greeting_updater(stub_grpc, doc, mongo_db):
    file = await upload_file(doc['greeting_avatar_id'], stub_grpc)
    if file:
        temp = await mongo_db.update_one({"_id": doc['_id']}, {"$set": {"greeting_avatar_id": file}})
        if temp == 0:
            print("err")

