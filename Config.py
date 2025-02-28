from enum import Enum
import os

import SecureConfig as scfg



# SERVER_PORT = 8765
# SERVER_HOST = "localhost"

SERVER_PORT = os.environ.get('PORT',  8765)
SERVER_HOST = "0.0.0.0"   #  "localhost"


# 3.75.158.163
# 3.125.183.140
# 35.157.117.28


DB_HOST = scfg.DB_HOST  
DB_PORT = scfg.DB_PORT
DB_USER = scfg.DB_USER
DB_PASSWORD = scfg.DB_PASSWORD
DB_NAME = scfg.DB_NAME


class operationTypes(Enum):
    LOGIN_INIT = 1
    CREATE_CHAT = 2
    WRITE_TO_CHAT = 3


class ReceivingOperTypes(Enum):
    # Receiving
    # USER_INIT = "user_init"
    USER_REGISTER = "user_register"
    USER_LOGIN = "user_login"
    USER_LOGIN_RESULT = "user_login_result"
    GAME_REQUEST = "game_request"

    GET_LOGIN_USERS = "get_login_users"
    CHAT_CREATE = "chat_create"
    CHAT_WRITE = "chat_write"
    GAME_REQUEST_TO = "game_request_to"
    GAME_REQUEST_ANSWER_FROM = "game_request_answer_from"


class SendingOperTypes(Enum):
    # Sending
    USER_GET_UUID = "user_get_uuid"
    USERS_ONLINE = "users_online"
    USER_LOGIN_ANS = "user_login_ans"
    USER_REGISTER_ANS = "user_register_ans"
    GAME_REQUEST_FROM = "game_request_from"
    GAME_REQUEST_ANSWER_TO = "game_request_answer_to"
    GAME_BEGIN = "game_begin"




