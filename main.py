import asyncio
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os

import Config as cfg
# import message_Handler as mh
# from utils import dbadapter as db
from ws import nServer as srv
from Catan import Game as cg

def main():  
    srv.Run()



    # class HTTPHandler(SimpleHTTPRequestHandler):
    #     """This handler uses server.base_path instead of always using os.getcwd()"""
    #
    #     def translate_path(self, path):
    #         path = SimpleHTTPRequestHandler.translate_path(self, path)
    #         relpath = os.path.relpath(path, os.getcwd())
    #         fullpath = os.path.join(self.server.base_path, relpath)
    #         return fullpath
    #
    # class HTTPServer(BaseHTTPServer):
    #     """The main server, you pass in base_path which is the path you want to serve requests from"""
    #
    #     def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
    #         self.base_path = base_path
    #         BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)
    #
    # web_dir = os.path.join(os.path.dirname(__file__), 'my_dir')
    # httpd = HTTPServer(web_dir, ("", os.environ.get('PORT',  8000)))
    # httpd.serve_forever()

########################################################

    game_server = cg.GameServer()
    game_server.start_game()

    # Попытка разместить поселение и дорогу
    game_server.build_settlement(0, 0, 0, player_id=1)
    game_server.build_road(0, 0, 0, player_id=1)
    game_server.build_settlement(0, 0, 0, player_id=2)  # Повторная попытка - должна быть занята



if __name__ == "__main__":
    main()
