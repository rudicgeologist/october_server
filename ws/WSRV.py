import uuid
import json
import asyncio

import websockets

import Config as cfg  


class WSRV:
    def __init__(self, host, port, dba):
        self.connected_users = {}
        self.host = host
        self.port = port
        self.dba = dba

    async def NotifyUsers(self):
        """Send the list of online users to all connected clients."""
        if self.connected_users:  # Only notify if there are users online
            # message = "Online users: " + ", ".join(self.connected_users.keys())
            _users = []
            for _uuid, usr in self.connected_users.items():
                _users.append({"uuid": _uuid, "login": usr[1]})
            print(_users)
            online_users = {
                "operation_tag": cfg.operTypes.USERS_ONLINE.value,
                "users": _users
            }
            print(online_users)
            message = json.dumps(online_users)
            # await asyncio.wait([user.send(message) for user in self.connected_users.values()])    # TODO user send
            await asyncio.gather(*[user[0].send(message) for user in self.connected_users.values()])

    async def DisconnectUser(self, websocket):
        """Unregister a user when they disconnect."""
        for usr in self.connected_users.values():
            if usr[0] == websocket:
                self.connected_users = {key: val for key, val in self.connected_users.items() if val[0] != websocket}
                print(f"del usr {usr[1]}")
        await self.NotifyUsers()

    async def HandleConnection(self, websocket, path):
        """Handle the user connection, message reception and disconnection."""
        print(f"Connected: {websocket}")
        try:
            async for message in websocket:
                mess = None
                try:
                    mess = json.loads(message)
                    print("---------")
                    print(mess)
                    print("---------")
                except ValueError as e:
                    print(f" ERROR json.loads: {str(ValueError)} ")
                finally:
                    await self.HandleMessage(mess, websocket)

        except websockets.exceptions.ConnectionClosed:
            print(f" ConnectionClosed: {str(websocket)} disconnected.")
            await self.DisconnectUser(websocket)
        finally:
            # Unregister user when they disconnect
            print(f" finally: {str(websocket)} disconnected.")
            await self.DisconnectUser(websocket)

    async def HandleMessage(self, message, websocket):
        print(message)
        # if hasattr(message, 'operation_tag'):
        if "operation_tag" in message:
            message_js = json.loads(str(message).replace("\'", "\""))
            operation_tag = message_js["operation_tag"]

            if operation_tag == cfg.operTypes.USER_REGISTER.value:
                _login = message["login"]
                _pass_hash = message["pass_hash"]
                _pass_salt = message["pass_salt"]
                user_uuid = await self.dba.registerUser(_login, _pass_hash, _pass_salt)
                if user_uuid is not None:
                    login_object = {
                        "status": "success"
                    }
                    await websocket.send(json.dumps(login_object))
                    print("register_OK")
                    await self.NotifyUsers()

                else:
                    print("register_ERROR")
                    login_object = {
                        "status": "error"
                    }
                    await websocket.send(json.dumps(login_object))


            if operation_tag == cfg.operTypes.USER_LOGIN.value:
                _login = message_js["login"]
                # _passH = message_js["passH"]
                # _uuid = message["uuid"]
                # result_login = await self.dba.loginUser(_login, _passH, _uuid)
                _password = await self.dba.loginUser(_login)        #, _passH)
                print(str(_password))
                # await websocket.send(_password)             #(json.dumps(_password))
                if _password is not None:
                    print(_password["hash"])
                    print(_password["salt"])
                    login_object = {
                        "status": "success",
                        "password": {
                            "hash": _password["hash"],
                            "salt": _password["salt"]
                        }
                    }
                    await websocket.send(json.dumps(login_object))
                #     print("LOGIN OK")
                #     self.connected_users[str(user_uuid)] = (websocket, _login)
                #     await self.NotifyUsers()
                #
                else:
                    print("login_ERROR")
                    login_object = {
                        "status": "error"
                    }
                    await websocket.send(json.dumps(login_object))


            if operation_tag == cfg.operTypes.CHAT_CREATE.value:
                _uuid_cr = message["uuid_cr"]
                _name = message["name"]
                phones_js = message["phones_js"]
                # result_create_chat = await self.dba.loginUser(_login, _passH, _uuid)
                # print(result_login)
                # if result_login:
                #     print("LOGIN OK")
                #     self.connected_users[_uuid] = websocket
                #     await self.NotifyUsers()
                # else:
                #     print("login_ERROR")



    async def StartServer(self):
        async with websockets.serve(self.HandleConnection, self.host, self.port):
            print(f"Server is running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever

    def Run(self):
        asyncio.run(self.StartServer())

