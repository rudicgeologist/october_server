import asyncio
import json
import sys

from Cubes import Game
import Config as cfg


class GameHandler:
    def __init__(self):
        self.games = []

    async def gamer_move(self, game_uuid, gamer_uuid, dscore):
        for game in self.games:
            if game.get_uuid() == game_uuid:
                for gamer in game.gamers:
                    if gamer.get_uuid() == gamer_uuid:
                        gamer.is_move_complete = True
                        gamer.score = gamer.score + dscore
                    # else:
                    gamer_move_notif_object = {
                        "operation_tag": cfg.SendingOperTypes.GAMER_MOVE_NOTIF.value,
                        "gamer_uuid": gamer_uuid,
                        "dice_score": dscore
                    }
                    print(f"gamer_move_notif_object: {gamer_move_notif_object}")
                    await gamer.get_websocket().send(json.dumps(gamer_move_notif_object))


    def add_game(self, users, _uuid):

        game = Game.Game(0, 2, users, _uuid)
        asyncio.create_task(game.send_game_notif())
        asyncio.create_task(game.start_game())  # asyncio.run asyncio.create_task
        self.games.append(game)
        # sys.stdout.write(f"New Game for users: {'-'.join(users)} \n")
        # sys.stdout.flush()
        return game



