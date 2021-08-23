from queue import Queue
from threading import Thread
from documents import *
import grpc
from skyproto_pb import media_pb2_grpc
from config import *
from src.db import Connection
from src.upload import upload_file


class Worker:
    def photo(self):
        res = Photo.objects(__raw__={"photo_content_id": {'$regex': 'http'}})
        print("photo", len(res))
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)

        queue = Queue()
        for item in res:
            queue.put(item)
        for i in range(COUNT_PHOTO_WORKER):
            print(i, "photo")
            t = WorkerThread(kind="photo", queue=queue, stub=stub)
            t.start()

    def message(self):
        res = DialogMessage.objects(__raw__={"$or": [{"message_content.data_id": {"$regex": "http"}},
                                                     {"message_content.preview_id": {"$regex": "http"}}]})
        print("message", len(res))
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)
        queue = Queue()
        for item in res:
            queue.put(item)
        for i in range(COUNT_MESSAGE_WORKER):
            print(i, "message")
            t = WorkerThread(kind="message", queue=queue, stub=stub)
            t.start()

    def user(self):
        res = User.objects(__raw__={"user_avatar.content_id": {"$regex": "http"}})
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)
        print("user", len(res))
        queue = Queue()
        for item in res:
            queue.put(item)
        for i in range(COUNT_USER_WORKER):
            print(i, "user")
            t = WorkerThread(kind="user", queue=queue, stub=stub)
            t.start()

    def chat_room(self):
        res = Room.objects(__raw__={"room_avatar_id": {"$regex": "http"}})
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)
        print("chat_room", len(res))
        queue = Queue()
        for item in res:
            queue.put(item)

        t = WorkerThread(kind="chat_room", queue=queue, stub=stub)
        t.start()

    def event(self):

        res = Event.objects(__raw__={"$or": [{"event_image.avatar.id": {"$regex": "http"}},
                                             {"event_image.cover.id": {"$regex": "http"}},
                                             {"event_image.banner.id": {"$regex": "http"}}
                                             ]})
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)
        print("event", len(res))
        queue = Queue()
        for item in res:
            queue.put(item)

        t = WorkerThread(kind="event", queue=queue, stub=stub)
        t.start()

    def greeting(self):
        res = Greetings.objects(__raw__={"greeting_avatar_id": {"$regex": "http"}})
        print("greeting", len(res))
        channel = grpc.insecure_channel(UPLOAD_GRPC_ADDRESS, options=(('grpc.max_concurrent_streams', -1),))
        stub = media_pb2_grpc.MediaStub(channel)
        queue = Queue()
        for item in res:
            queue.put(item)

        t = WorkerThread(kind="greeting", queue=queue, stub=stub)
        t.start()


class WorkerThread(Thread):

    def __init__(self, kind, queue, stub = None):
        """Инициализация потока"""
        Thread.__init__(self)
        self.con = Connection()
        self.file_kind = kind
        self.task = queue
        self.stub_grpc = stub

    def run(self):
        """Запуск потока"""
        while self.task.qsize() > 0:
            update_object(kind=self.file_kind, item=self.task.get(), stub_grpc=self.stub_grpc)



def update_object(kind, item, stub_grpc):
    try:
        if kind == 'photo':
            file = upload_file(item.photo_content_id,stub_grpc)
            if file:
                temp = Photo.objects(id=item.id).update_one(photo_content_id=file)
                if temp == 0:
                    print("err")

        elif kind == 'user':
            file = upload_file(item.user_avatar.content_id,stub_grpc)
            if file:
                temp = User.objects(id=item.id).update_one(user_avatar__content_id=file)
                if temp == 0:
                    print("err")

        elif kind == 'chat_room':
            file = upload_file(item.room_avatar_id,stub_grpc)
            if file:
                temp = Room.objects(id=item.id).update_one(room_avatar_id=file)
                if temp == 0:
                    print("err")

        elif kind == 'message':
            if item.message_content.data_id != "" and item.message_content.preview_id != "":
                data_id = upload_file(item.message_content.data_id,stub_grpc)
                preview_id = upload_file(item.message_content.preview_id,stub_grpc)
                if data_id and preview_id:
                    temp = DialogMessage.objects(id=item.id).update_one(
                        message_content__data_id=data_id,
                        message_content__preview_id=preview_id)
                    if temp == 0:
                        print("err")
            elif item.message_content.data_id != "":
                data_id = upload_file(item.message_content.data_id,stub_grpc)
                if data_id:
                    temp = DialogMessage.objects(id=item.id).update_one(
                        message_content__data_id=data_id)
                    if temp == 0:
                        print("err")

        elif kind == 'event':
            print("in event", item.event_image.cover.id)
            cover = upload_file(item.event_image.cover.id,stub_grpc)
            banner = upload_file(item.event_image.banner.id,stub_grpc)
            avatar = upload_file(item.event_image.avatar.id,stub_grpc)
            print("!!!!!!", cover, banner, avatar)
            if cover and banner and avatar:
                temp = Event.objects(id=item.id).update(__raw__={"$set": {"event_image.avatar.id": avatar,
                                                                          "event_image.cover.id": cover,
                                                                          "event_image.banner.id": banner}})
                print(temp)
                if temp == 0:
                    print("err")

        elif kind == 'greeting':
            file = upload_file(item.greeting_avatar_id,stub_grpc)
            if file:
                temp = Greetings.objects(id=item.id).update_one(greeting_avatar_id=file)
                if temp == 0:
                    print("err")

    except BaseException as e:
        print(e, flush=True)

