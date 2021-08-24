import time
from src.workers.photo import photos
from src.workers.user import users
from src.workers.event import events
from src.workers.dialog_messages import messages
from src.workers.chat_room import chat_rooms
from src.workers.greeting import greetings
from asyncio import wait, get_event_loop


if __name__ == '__main__':
    times = time.time()
    loop = get_event_loop()
    tasks = [
        greetings(),
        events(),
        messages(),
        photos(),
        chat_rooms(),
        users()
    ]
    loop.run_until_complete(wait(tasks))
    print(time.time()-times)
    loop.close()
