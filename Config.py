from enum import Enum

import SecureConfig as scfg

PORT = 15555
HOST = "localhost"

SERVER_PORT = 8765
SERVER_HOST = "localhost"


DB_HOST = scfg.DB_HOST  
DB_PORT = scfg.DB_PORT
DB_USER = scfg.DB_USER
DB_PASSWORD = scfg.DB_PASSWORD
DB_NAME = scfg.DB_NAME


class operationTypes(Enum):
    LOGIN_INIT = 1
    CREATE_CHAT = 2
    WRITE_TO_CHAT = 3


class operTypes(Enum):
    # Receiving
    # USER_INIT = "user_init"
    USER_REGISTER = "user_register"
    USER_LOGIN = "user_login"
    CHAT_CREATE = "chat_create"
    CHAT_WRITE = "chat_write"

    # Sending
    USER_GET_UUID = "user_get_uuid"
    USERS_ONLINE = "users_online"




