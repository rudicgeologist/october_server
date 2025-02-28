import asyncio
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os

import Config as cfg
# import message_Handler as mh
# from utils import dbadapter as db
from ws import nServer as srv
from Catan import Game as cg
from Cubes import Game as cbh
from Cubes import Move as mv
from Cubes import GameHandler as gh



def main():
    # dh = h.Handler()
    # print(dh.roll_dice(4))

    # move = mv.Move(5)
    # dices = move.roll_dice(5)
    # move.get_combination(dices)

#####################
    _gh = gh.GameHandler()
    srv.Run(_gh)

    # game_server = cg.GameServer()
    # game_server.start_game()
    #
    # # Попытка разместить поселение и дорогу
    # game_server.build_settlement(0, 0, 0, player_id=1)
    # game_server.build_road(0, 0, 0, player_id=1)
    # game_server.build_settlement(0, 0, 0, player_id=2)  # Повторная попытка - должна быть занята
#############


if __name__ == "__main__":
    main()
