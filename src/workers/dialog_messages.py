from skyproto_pb import media_pb2_grpc
from src.db import MongoDBConnection
from src.upload import upload_file
from asyncio import create_task
from src.grpc import channel
from config import START_FROM, LIMIT


async def messages():
    mongo_client = MongoDBConnection().client
    mongo_db = mongo_client.chat_db
    res = mongo_db['dialog_message'].find({"$or": [{"message_content.data_id": {"$regex": "http"}},
                                                   {"message_content.preview_id": {"$regex": "http"}}]}).skip(START_FROM).limit(START_FROM+LIMIT)

    stub_grpc = media_pb2_grpc.MediaStub(channel)
    tasks = []
    async for item in res:
        tasks.append(create_task(messages_updater(stub_grpc, item, mongo_db['dialog_message'])))

    for task in tasks:
        await task
    print('messages end')


async def messages_updater(stub_grpc, doc, mongo_db):
    if doc['message_content']['data_id'] != "" and doc['message_content']['preview_id'] != "":
        data_id = await upload_file(doc['message_content']['data_id'], stub_grpc)
        preview_id = await upload_file(doc['message_content']['preview_id'], stub_grpc)
        if data_id and preview_id:
            temp = await mongo_db.update_one({"_id": doc['_id']},
                                             {"$set": {"message_content__data_id": data_id,
                                                       "message_content__preview_id": preview_id}})
            if temp == 0:
                print("err")
    elif doc['message_content']['data_id'] != "":
        data_id = await upload_file(doc['message_content']['data_id'], stub_grpc)
        if data_id:
            temp = await mongo_db.update_one({"_id": doc['_id']},
                                             {"$set": {"message_content__data_id": data_id}})
            if temp == 0:
                print("err")

