import sys
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
            sys.stdout.write(f"_users: \n {_users} \n")
            sys.stdout.flush()
            online_users = {
                "operation_tag": cfg.operTypes.USERS_ONLINE.value,
                "users": _users
            }
            sys.stdout.write(f"_online_users: \n {online_users} \n")
            sys.stdout.flush()
            message = json.dumps(online_users)
            # await asyncio.wait([user.send(message) for user in self.connected_users.values()])    # TODO user send
            await asyncio.gather(*[user[0].send(message) for user in self.connected_users.values()])

    async def DisconnectUser(self, websocket):
        """Unregister a user when they disconnect."""
        for usr in self.connected_users.values():
            if usr[0] == websocket:
                self.connected_users = {key: val for key, val in self.connected_users.items() if val[0] != websocket}
                sys.stdout.write(f"del usr {usr[1]} \n")
                sys.stdout.flush()
        await self.NotifyUsers()

    async def HandleConnection(self, websocket, path):
        """Handle the user connection, message reception and disconnection."""
        sys.stdout.write(f"SERVER_HANDLE_CONNECTION Connected: {websocket} \n")
        sys.stdout.flush()
        try:
            async for message in websocket:
                mess = None
                try:
                    mess = json.loads(message)
                except ValueError as e:
                    sys.stdout.write(f" ERROR json.loads: {str(ValueError)} \n")
                    sys.stdout.flush()
                finally:
                    await self.HandleMessage(mess, websocket)

        except websockets.exceptions.ConnectionClosed:
            sys.stdout.write(f"SERVER_HANDLE_CONNECTION ConnectionClosed: {str(websocket)}\n")
            sys.stdout.flush()
            await self.DisconnectUser(websocket)
        finally:
            # Unregister user when they disconnect
            sys.stdout.write(f"SERVER_HANDLE_CONNECTION disconnected: {str(websocket)}\n")
            sys.stdout.flush()
            await self.DisconnectUser(websocket)

    async def HandleMessage(self, message, websocket):
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
                    sys.stdout.write(f"register_OK \n")
                    sys.stdout.flush()
                    await self.NotifyUsers()

                else:

                    sys.stdout.write(f"register_ERROR \n")
                    sys.stdout.flush()
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
                # await websocket.send(_password)             #(json.dumps(_password))
                if _password is not None:
                    login_object = {
                        "status": "success",
                        "password": {
                            "hash": _password["hash"],
                            "salt": _password["salt"]
                        }
                    }
                    await websocket.send(json.dumps(login_object))
                else:
                    sys.stdout.write(f"login_ERROR \n")
                    sys.stdout.flush()
                    login_object = {
                        "status": "error"
                    }
                    await websocket.send(json.dumps(login_object))


            if operation_tag == cfg.operTypes.CHAT_CREATE.value:
                _uuid_cr = message["uuid_cr"]
                _name = message["name"]
                phones_js = message["phones_js"]

    async def StartServer(self):
        async with websockets.serve(self.HandleConnection, self.host, self.port):
            sys.stdout.write(f"Server is running on ws://{self.host}:{self.port} \n")
            sys.stdout.flush()
            await asyncio.Future()  # Run forever

    def Run(self):
        asyncio.run(self.StartServer())

