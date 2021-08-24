from skyproto_pb import media_pb2_grpc
from src.db import MongoDBConnection
from src.upload import upload_file
from asyncio import create_task
from src.grpc import channel
from config import START_FROM, LIMIT


async def users():
    mongo_client = MongoDBConnection().client
    mongo_db = mongo_client.profile_db
    res = mongo_db['user'].find({"user_avatar.content_id": {"$regex": "http"}}).skip(START_FROM).limit(START_FROM+LIMIT)
    stub_grpc = media_pb2_grpc.MediaStub(channel)

    tasks = []
    async for item in res:
        #tasks.append(create_task(user_updater(stub_grpc, item, mongo_db['user'])))
        await user_updater(stub_grpc, item, mongo_db['user'])

    #for task in tasks:
    #    await task
    print('user end')


async def user_updater(stub_grpc, doc, mongo_db):
    file = await upload_file(doc['user_avatar']['content_id'], stub_grpc)
    if file:
        temp = await mongo_db.update_one({"_id": doc['_id']}, {"$set": {"user_avatar__content_id": file}})
        if temp == 0:
            print("err")

