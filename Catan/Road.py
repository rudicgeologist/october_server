class Road:
    def __init__(self, owner: int):
        self.owner = owner  # ID игрока

    def __repr__(self):
        return f"Road by player {self.owner}"
