import asyncio

import Config as cfg
# import message_Handler as mh
# from utils import dbadapter as db
from ws import nServer as srv
from Catan import Game as cg

def main():  
    srv.Run()

    game_server = cg.GameServer()
    game_server.start_game()

    # Попытка разместить поселение и дорогу
    game_server.build_settlement(0, 0, 0, player_id=1)
    game_server.build_road(0, 0, 0, player_id=1)
    game_server.build_settlement(0, 0, 0, player_id=2)  # Повторная попытка - должна быть занята



if __name__ == "__main__":
    main()
