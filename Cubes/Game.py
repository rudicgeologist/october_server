import asyncio
import json
import random
import sys
import time

from Cubes.Gamer import Gamer

import Config as cfg


class Game:
    def __init__(self, hparam: int, max_gamers: int, users: [], uuid):
        print('Game create')
        self.id = 0
        self.hparam = hparam
        self.max_gamers = max_gamers
        # self.users = users
        self.gamers = []
        self.uuid = uuid
        for usr in users:
            # gamer_object = {
            #     "uuid": usr["uuid"],
            #     "login": usr["login"],
            #     "websocket": usr["websocket"],
            #     "score": 0
            # }
            gamer = Gamer(usr["uuid"], usr["login"], usr["websocket"])
            self.gamers.append(gamer)

        self.current_player_moving = None
        self.isStarted = False

    def get_uuid(self):
        return self.uuid

    async def send_game_notif(self):  # , users: []):
        print("send_game_notif")
        _users = []
        for gamer in self.gamers:
            user_object = {
                "uuid": gamer.get_uuid(),
                "login": gamer.get_login()
            }
            _users.append(user_object)

        game_begin_object = {
            "operation_tag": cfg.SendingOperTypes.GAME_BEGIN.value,
            "status": "success",
            "uuid": self.uuid,
            "users": _users
        }
        for gamer in self.gamers:  # TODO user send
            await gamer.get_websocket().send(json.dumps(game_begin_object))

    async def start_game(self):  # async
        self.isStarted = True
        sys.stdout.write(f"self.gamers: {self.gamers}\n")
        sys.stdout.flush()

        while not self.is_game_over():
            for gamer in self.gamers:
                # print(gamer)
                # await asyncio.sleep(3)
                await gamer.move()

    def is_game_over(self):
        for gamer in self.gamers:
            if gamer.get_score() >= 300:    # TODO == 1000
                return True

        return False

    def roll_dice(self, dice_count: int):
        result = []
        dice = 0
        while dice < dice_count:
            dice_res = random.randint(1, 6)
            sys.stdout.write(f"dice_res {dice_res} \n")
            sys.stdout.flush()

            Adice = (dice, dice_res)
            result.append(Adice)
            dice = dice + 1
        return result
