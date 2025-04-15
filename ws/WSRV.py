import pathlib
import ssl
import sys
import time
import uuid
import json
import asyncio

import websockets

import Config as cfg
# from Cubes.Gamer import Gamer


class WSRV:
    def __init__(self, host, port, dba, _gh):
        self.logged_in_users = {}
        self.login_users = []
        self.gamers = []
        self.host = host
        self.port = port
        self.dba = dba
        self._gh = _gh

    async def notify_users(self):
        get_login_users_object = {
            "operation_tag": cfg.SendingOperTypes.USERS_ONLINE.value,
            "users": []
        }
        for usr in self.login_users:
            ausr = {
                "user_login": usr["user_login"],
                "user_uuid": usr["user_uuid"]
            }
            get_login_users_object["users"].append(ausr)
        sys.stdout.write(f"{get_login_users_object} \n")
        sys.stdout.flush()

        for user in self.login_users:
            await user["user_websocket"].send(json.dumps(get_login_users_object))

        # await websocket.send(json.dumps(get_login_users_object))
        # await asyncio.gather(*[user[0].send(message) for user in self.logged_in_users.values()])

    # async def NotifyUsers(self):
    #     if self.logged_in_users:  # Only notify if there are users online
    #         # message = "Online users: " + ", ".join(self.connected_users.keys())
    #         _users = []
    #         for _uuid, usr in self.logged_in_users.items():
    #             _users.append({"uuid": _uuid, "login": usr[1]})
    #         sys.stdout.write(f"_users: \n {_users} \n")
    #         sys.stdout.flush()
    #         online_users = {
    #             "operation_tag": cfg.ReceivingOperTypes.USERS_ONLINE.value,
    #             "users": _users
    #         }
    #         sys.stdout.write(f"_online_users: \n {online_users} \n")
    #         sys.stdout.flush()
    #         message = json.dumps(online_users)
    #         # await asyncio.wait([user.send(message) for user in self.connected_users.values()])    # TODO user send
    #         await asyncio.gather(*[user[0].send(message) for user in self.logged_in_users.values()])

    async def DisconnectUser(self, websocket):
        # """Unregister a user when they disconnect."""
        # for usr in self.logged_in_users.values():
        #     if usr[0] == websocket:
        #         self.logged_in_users = {key: val for key, val in self.logged_in_users.items() if val[0] != websocket}
        #         sys.stdout.write(f"    self.connected_users: {self.logged_in_users}")
        #         sys.stdout.flush()
        #         sys.stdout.write(f"del usr {usr[1]} \n")
        #         sys.stdout.flush()

        for usr in self.login_users:
            if usr["user_websocket"] == websocket:
                self.login_users.remove(usr)
                sys.stdout.write(f"------------------------------------------------------------------------------------\n")
                sys.stdout.flush()
                sys.stdout.write(f"DISCONNECT:    self.login_users: {self.login_users} \n")
                sys.stdout.flush()

        # await self.NotifyUsers()
        await self.notify_users()

    async def HandleConnection(self, websocket, path):
        sys.stdout.write(f"------------------------------------------------------------------------------------\n")
        sys.stdout.flush()
        sys.stdout.write(f"SERVER_HANDLE_CONNECTION Connected: {websocket} \n")
        sys.stdout.flush()
        sys.stdout.write(f"CONNECT:    self.login_users: {self.login_users} \n")
        sys.stdout.flush()
        # sys.stdout.write(f"self.login_users: {self.login_users} \n")
        # sys.stdout.flush()
        try:
            async for message in websocket:
                sys.stdout.write(f"message: {message} \n")
                sys.stdout.flush()
                mess = None
                try:
                    mess = json.loads(message)
                except ValueError as e:
                    sys.stdout.write(f" ERROR json.loads: {str(ValueError)} \n")
                    sys.stdout.flush()
                finally:
                    await self.HandleMessage(mess, websocket)

        except websockets.exceptions.ConnectionClosed:
            sys.stdout.write(f"------------------------------------------------------------------------------------\n")
            sys.stdout.flush()
            sys.stdout.write(f"SERVER_HANDLE_CONNECTION ConnectionClosed: {str(websocket)}\n")
            sys.stdout.flush()
            await self.DisconnectUser(websocket)
        finally:
            # Unregister user when they disconnect
            sys.stdout.write(f"------------------------------------------------------------------------------------\n")
            sys.stdout.flush()
            sys.stdout.write(f"SERVER_HANDLE_CONNECTION disconnected: {str(websocket)}\n")
            sys.stdout.flush()
            await self.DisconnectUser(websocket)

    async def HandleMessage(self, message, websocket):
        # print(f"HandleMessage: {message}")
        if message is not None:
            # if hasattr(message, 'operation_tag'):
            if "operation_tag" in message:
                message_js = json.loads(str(message).replace("\'", "\""))
                operation_tag = message_js["operation_tag"]

                if operation_tag == cfg.ReceivingOperTypes.GET_LOGIN_USERS.value:
                    await self.notify_users()

                if operation_tag == cfg.ReceivingOperTypes.USER_REGISTER.value:
                    _login = message["login"]
                    _pass_hash = message["pass_hash"]
                    _pass_salt = message["pass_salt"]
                    user_uuid = await self.dba.registerUser(_login, _pass_hash, _pass_salt)
                    if user_uuid is not None:
                        login_object = {
                            "operation_tag": cfg.SendingOperTypes.USER_REGISTER_ANS.value,
                            "status": "success"
                        }
                        await websocket.send(json.dumps(login_object))
                        sys.stdout.write(f"register_OK \n")
                        sys.stdout.flush()
                        # await self.NotifyUsers()

                    else:
                        sys.stdout.write(f"register_ERROR \n")
                        sys.stdout.flush()
                        login_object = {
                            "operation_tag": cfg.SendingOperTypes.USER_REGISTER_ANS.value,
                            "status": "error"
                        }
                        await websocket.send(json.dumps(login_object))

                if operation_tag == cfg.ReceivingOperTypes.USER_LOGIN.value:
                    _login = message_js["login"]
                    # _passH = message_js["passH"]
                    # _uuid = message["uuid"]
                    # result_login = await self.dba.loginUser(_login, _passH, _uuid)
                    _login_preresult = await self.dba.loginUser(_login)  # , _passH)
                    # await websocket.send(_login_preresult)             #(json.dumps(_login_preresult))
                    print(f"_login: {_login}")
                    # time.sleep(3)
                    if _login_preresult["_uuid"] is not None:
                        login_object = {
                            "operation_tag": cfg.SendingOperTypes.USER_LOGIN_ANS.value,
                            "status": "success",
                            "password": {
                                "hash": _login_preresult["hash"],
                                "salt": _login_preresult["salt"],
                                "_uuid": str(_login_preresult["_uuid"])
                            }
                        }
                        await websocket.send(json.dumps(login_object))
                    else:
                        sys.stdout.write(f"login_ERROR \n")
                        sys.stdout.flush()
                        login_object = {
                            "operation_tag": cfg.SendingOperTypes.USER_LOGIN_ANS.value,
                            "status": "error"
                        }
                        await websocket.send(json.dumps(login_object))

                if operation_tag == cfg.ReceivingOperTypes.USER_LOGIN_RESULT.value:
                    sys.stdout.write(f"USER_LOGIN_RESULT \n")
                    sys.stdout.flush()
                    if message["status"] == "success":
                        AUser = {
                            "user_login": message["login"],
                            "user_uuid": message["user_uuid"],
                            "user_websocket": websocket
                        }
                        self.login_users.append(AUser)

                        # AGamer = Gamer(message["login"], message["user_uuid"], websocket)
                        # self.gamers.append(AGamer)

                        await self.notify_users()
                        sys.stdout.write(f"{self.login_users} \n")
                        sys.stdout.flush()

                if operation_tag == cfg.ReceivingOperTypes.GAME_REQUEST_TO.value:
                    user_rec = message_js["second_user_uuid"]

                    f_user = next((user for user in self.login_users if user["user_uuid"] == user_rec), None)
                    s_user = next((user for user in self.login_users if user["user_websocket"] == websocket), None)

                    # for user in self.login_users:
                    #     if user["user_uuid"] == user_rec:
                    #         for usr in self.login_users:
                    #             if usr["user_websocket"] == websocket:
                    game_request_object = {
                        "operation_tag": cfg.SendingOperTypes.GAME_REQUEST_FROM.value,
                        "init_request_user_uuid": s_user["user_uuid"]
                    }
                    await f_user["user_websocket"].send(json.dumps(game_request_object))

                if operation_tag == cfg.ReceivingOperTypes.GAME_REQUEST_ANSWER_FROM.value:
                    # TODO status: success
                    user_ans = message_js["first_user_uuid"]
                    users = []
                    users_g = []

                    f_user = next((user for user in self.login_users if user["user_uuid"] == user_ans), None)
                    print(f'f_user: {f_user}')
                    user_object = {
                        "login": f_user["user_login"],
                        "uuid": f_user["user_uuid"],
                        "websocket": f_user["user_websocket"],
                    }
                    users.append(user_object)
                    users_g.append({"uuid": f_user["user_uuid"]})

                    s_user = next((user for user in self.login_users if user["user_websocket"] == websocket), None)
                    print(f's_user: {s_user}')
                    user_object = {
                        "login": s_user["user_login"],
                        "uuid": s_user["user_uuid"],
                        "websocket": s_user["user_websocket"],
                    }
                    users.append(user_object)
                    users_g.append({"uuid": s_user["user_uuid"]})

                    game_uuid = await self.dba.create_game(users_g)

                    game = self._gh.add_game(users, game_uuid)
                    # game.start_game()

                    # game_begin_object = {
                    #     "operation_tag": cfg.SendingOperTypes.GAME_BEGIN.value,
                    #     "status": "success",
                    #     "users": users
                    # }
                    # print(game_begin_object)
                    # await f_user["user_websocket"].send(json.dumps(game_begin_object))
                    # await s_user["user_websocket"].send(json.dumps(game_begin_object))

                if operation_tag == cfg.ReceivingOperTypes.GAMER_MOVE_ANS.value:
                    game_uuid = message_js["game_uuid"]
                    gamer_uuid = message_js["gamer_uuid"]
                    dice_score = message_js["dice_score"]
                    await self._gh.gamer_move(game_uuid, gamer_uuid, dice_score)




                # if operation_tag == cfg.ReceivingOperTypes.GAME_REQUEST_TO.value:
                #     pass
                #
                # if operation_tag == cfg.ReceivingOperTypes.CHAT_CREATE.value:
                #     _uuid_cr = message["uuid_cr"]
                #     _name = message["name"]
                #     phones_js = message["phones_js"]

    async def StartServer(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
        ssl_context.load_cert_chain(localhost_pem)
        async with websockets.serve(self.HandleConnection, self.host, self.port):  # , ssl=ssl_context):
            sys.stdout.write(f"Server is running on ws://{self.host}:{self.port} \n")
            sys.stdout.flush()
            await asyncio.Future()  # Run forever

    def Run(self):
        # asyncio.run(self.StartServer())
        asyncio.create_task(self.StartServer())
