import asyncio
import json
import datetime


import Config as cfg

class Gamer:
    def __init__(self, uuid: str, login: str, websocket):
        self.uuid = uuid
        self.login = login
        self.websocket = websocket
        self.score = 0
        self.is_move_complete = False
        # self.websocket

    def get_uuid(self):
        return self.uuid

    def get_login(self):
        return self.login

    def get_websocket(self):
        return self.websocket

    def get_score(self):
        return self.score

    def set_move_complete(self, value):
        self.is_move_complete = value

    async def looper(self):
        while not self.is_move_complete:
            # print(f"{datetime.datetime.now()}: looper: {self.login} {self.uuid}")
            await asyncio.sleep(4)

    async def move(self):
        self.is_move_complete = False
        gamer_move_object = {         # TODO
            "operation_tag": cfg.SendingOperTypes.GAMER_MOVE.value
        }
        print("--MOVING--")
        print(f"{datetime.datetime.now()}: send to client {self.login} {self.uuid}")
        # print(game_request_object)
        # tasks = asyncio.all_tasks()
        # print("=== Current tasks in event loop ===")
        # for task in tasks:
        #     print(f"Task: {task.get_name()}, running: {not task.done()}")
        # print("==================================")
        await self.websocket.send(json.dumps(gamer_move_object))
        # print(f"{datetime.datetime.now()}: sleep")
        await asyncio.sleep(2)
        # print(f"{datetime.datetime.now()}: looper")
        await self.looper()  # asyncio.sleep(5)
        # asyncio.create_task(self.looper())

        print(f"{datetime.datetime.now()}: loop finshed {self.login} {self.uuid}")
        # print(f"    {self.websocket}: moved!")
        # send to client "moving"

        # await asyncio.sleep(600)
        # future = asyncio.create_task(self.looper())





