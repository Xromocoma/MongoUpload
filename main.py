from threading import Thread
from src.db import Connection
from src.worker import Worker


class FatherThread(Thread):
    def __init__(self, kind):
        Thread.__init__(self)
        self.con = Connection()
        self.worker = Worker()
        self.file_kind = kind

    def run(self):
        if self.file_kind == 'photo':
            self.worker.photo()
        elif self.file_kind == 'user':
            self.worker.user()
        elif self.file_kind == 'chat_room':
            self.worker.chat_room()
        elif self.file_kind == 'message':
            self.worker.message()
        elif self.file_kind == 'event':
            self.worker.event()
        elif self.file_kind == 'greeting':
            self.worker.greeting()
        print(f"Родитель `{self.file_kind}` закончил работу ", flush=True)


def main():

    kind = ['photo', 'user', 'chat_room', 'message', 'event', 'greeting']
    for i in kind:
        t = FatherThread(i)
        t.start()


if __name__ == '__main__':
    main()
