from typing import Optional

class Tile:
    def __init__(self, resource: str, number: Optional[int] = None):
        self.resource = resource 
        self.number = number

    def __repr__(self):
        return f"Tile({self.resource}, {self.number})"