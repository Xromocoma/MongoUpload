from os import getenv, path
import dotenv
dotenv.load_dotenv(
    path.join(path.dirname(__file__), '.env')
)

KAFKA_TOPIC = getenv('KAFKA_TOPIC')
KAFKA_GROUP_ID = getenv('KAFKA_GROUP_ID')
KAFKA_HOST = getenv('KAFKA_HOST')
KAFKA_PORT = int(getenv('KAFKA_PORT'))

MONGO_USER = getenv('MONGO_USER')
MONGO_PASSWORD = getenv('MONGO_PASSWORD')
MONGO_HOST = getenv('MONGO_HOST')
MONGO_PORT = int(getenv('MONGO_PORT'))

COUNT_PHOTO_WORKER = int(getenv('COUNT_PHOTO_WORKER'))
COUNT_MESSAGE_WORKER = int(getenv('COUNT_MESSAGE_WORKER'))
COUNT_USER_WORKER = int(getenv('COUNT_USER_WORKER'))

UPLOAD_GRPC_ADDRESS = getenv('UPLOAD_GRPC_ADDRESS','dev-svc.sl:8002')  # host:port