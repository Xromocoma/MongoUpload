from os import getenv, path
import dotenv

dotenv.load_dotenv(
    path.join(path.dirname(__file__), '.env')
)

MONGO_USER = getenv('MONGO_USER', 'usr')
MONGO_PASSWORD = getenv('MONGO_PASSWORD', '')
MONGO_HOST = getenv('MONGO_HOST', '')
MONGO_PORT = int(getenv('MONGO_PORT', '27017'))

COUNT_PHOTO_WORKER = int(getenv('COUNT_PHOTO_WORKER', '30'))
COUNT_MESSAGE_WORKER = int(getenv('COUNT_MESSAGE_WORKER', '30'))
COUNT_USER_WORKER = int(getenv('COUNT_USER_WORKER', '30'))

UPLOAD_GRPC_ADDRESS = getenv('UPLOAD_GRPC_ADDRESS', '')  # host:port

START_FROM = int(getenv('START_FROM', 0))
LIMIT = int(getenv('LIMIT', 20))
