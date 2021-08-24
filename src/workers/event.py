from skyproto_pb import media_pb2_grpc
from src.db import MongoDBConnection
from src.upload import upload_file
from asyncio import create_task
from src.grpc import channel
from config import START_FROM, LIMIT


async def events():
    mongo_client = MongoDBConnection().client
    mongo_db = mongo_client.event_db
    res = mongo_db['event'].find({"$or": [{"event_image.avatar.id": {"$regex": "http"}},
                                          {"event_image.cover.id": {"$regex": "http"}},
                                          {"event_image.banner.id": {"$regex": "http"}}
                                          ]}).skip(START_FROM).limit(START_FROM+LIMIT)
    stub_grpc = media_pb2_grpc.MediaStub(channel)

    tasks = []
    async for item in res:
        #tasks.append(create_task(event_updater(stub_grpc, item, mongo_db['event'])))
        event_updater(stub_grpc, item, mongo_db['event'])
    #for task in tasks:
    #    await task
    print('event end')


async def event_updater(stub_grpc, doc, mongo_db):
    print("in event", doc['event_image']['cover']['id'])
    cover = upload_file(doc['event_image']['cover']['id'], stub_grpc)
    banner = upload_file(doc['event_image']['banner']['id'], stub_grpc)
    avatar = upload_file(doc['event_image']['avatar']['id'], stub_grpc)
    print("!!!!!!", cover, banner, avatar)
    if cover and banner and avatar:
        temp = await mongo_db.update_one({"_id": doc['_id']}, {"$set": {"event_image.avatar.id": avatar,
                                                                  "event_image.cover.id": cover,
                                                                  "event_image.banner.id": banner}})
        print(temp)
        if temp == 0:
            print("err")

