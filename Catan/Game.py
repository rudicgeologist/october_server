from Catan import Board

class GameServer:
    def __init__(self):
        self.board = Board()

    def start_game(self):
        print("Starting game with board:")
        self.board.display()

    def build_settlement(self, row: int, col: int, corner: int, player_id: int):
        """Строит поселение или город игрока."""
        success = self.board.place_settlement(row, col, corner, player_id)
        if success:
            print(f"Player {player_id} построил поселение на ({row}, {col}, {corner})")
        else:
            print(f"Не удалось построить поселение на ({row}, {col}, {corner}): место занято.")

    def build_road(self, row: int, col: int, side: int, player_id: int):
        """Строит дорогу игрока."""
        success = self.board.place_road(row, col, side, player_id)
        if success:
            print(f"Player {player_id} построил дорогу на ({row}, {col}) стороне {side}") 
        else:
            print(f"Не удалось построить дорогу на ({row}, {col}) стороне {side}: место занято.")




