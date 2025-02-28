import sys

from Cubes import Game


class GameHandler:
    def __init__(self):
        self.games = []

    def add_game(self, users):
        game = Game.Game(0, 2, users)
        game.start_game()
        self.games.append(game)
        # sys.stdout.write(f"New Game for users: {'-'.join(users)} \n")
        # sys.stdout.flush()
        return game



