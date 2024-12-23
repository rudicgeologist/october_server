import random
from typing import List, Tuple, Optional, Dict


# Ресурсы и другие параметры поля
RESOURCES = ["wood", "brick", "sheep", "wheat", "ore", "desert"]
TILE_NUMBERS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
BOARD_LAYOUT = [3, 4, 5, 4, 3]  # Структура поля


class Tile:
    def __init__(self, resource: str, number: Optional[int] = None):
        self.resource = resource
        self.number = number

    def __repr__(self):
        return f"Tile({self.resource}, {self.number})" 


class Settlement:
    def __init__(self, owner: int, is_city: bool = False):
        self.owner = owner   # ID игрока
        self.is_city = is_city  # Флаг, является ли поселение городом

    def upgrade_to_city(self):
        """Преобразует поселение в город."""
        self.is_city = True

    def __repr__(self):
        return "City" if self.is_city else "Settlement"


class Road:
    def __init__(self, owner: int):
        self.owner = owner  # ID игрока

    def __repr__(self):
        return f"Road by player {self.owner}"


class Board:
    def __init__(self):
        self.tiles = self.generate_board()
        self.vertices = self.initialize_vertices()
        self.edges = self.initialize_edges()

    def generate_board(self) -> List[List[Tile]]:
        """Генерация случайного распределения ресурсов и чисел."""
        resources = ["wood"] * 4 + ["brick"] * 3 + ["sheep"] * 4 + ["wheat"] * 4 + ["ore"] * 3 + ["desert"]
        random.shuffle(resources)
        tile_numbers = TILE_NUMBERS.copy()
        random.shuffle(tile_numbers)

        board = []
        for row_size in BOARD_LAYOUT:
            row = []
            for _ in range(row_size):
                resource = resources.pop()
                number = None if resource == "desert" else tile_numbers.pop()
                row.append(Tile(resource, number))
            board.append(row)
        return board

    def initialize_vertices(self) -> Dict[Tuple[int, int], Optional[Settlement]]:
        """
        Инициализация узлов (вершин) для возможного размещения поселений.
        Каждая вершина обозначается кортежем (x, y).
        """
        vertices = {}
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                for corner in range(6):
                    # Кортеж (row, col, corner) обозначает конкретную вершину на шестиугольнике
                    vertices[(row, col, corner)] = None
        return vertices

    def initialize_edges(self) -> Dict[Tuple[int, int, int, int], Optional[Road]]:
        """
        Инициализация ребер (сторон) для возможного размещения дорог.
        Каждое ребро обозначается кортежем ((row1, col1), (row2, col2)) - между двумя тайлами.
        """
        edges = {}
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                for side in range(6):
                    # Кортеж ((row, col), side) - уникально обозначает ребро
                    edges[((row, col), side)] = None
        return edges

    def place_settlement(self, row: int, col: int, corner: int, owner: int, as_city=False) -> bool:
        """
        Попытка разместить поселение или город на вершине определенного тайла.
        """
        if self.vertices[(row, col, corner)] is None:
            self.vertices[(row, col, corner)] = Settlement(owner, is_city=as_city)
            return True
        return False

    def place_road(self, row: int, col: int, side: int, owner: int) -> bool:
        """
        Попытка построить дорогу на стороне тайла.
        """
        if self.edges[((row, col), side)] is None:
            self.edges[((row, col), side)] = Road(owner)
            return True
        return False

    def display(self):
        """Простое отображение доски в консоли."""
        for row in self.tiles:
            print(" ".join([f"{tile.resource[:3]}({tile.number or ' '})" for tile in row]))


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


# Пример работы
if __name__ == "__main__":
    game_server = GameServer()
    game_server.start_game()

    # Попытка разместить поселение и дорогу
    game_server.build_settlement(0, 0, 0, player_id=1)
    game_server.build_road(0, 0, 0, player_id=1)
    game_server.build_settlement(0, 0, 0, player_id=2)  # Повторная попытка - должна быть занята
