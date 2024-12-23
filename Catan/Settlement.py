class Settlement:
    def __init__(self, owner: int, is_city: bool = False):
        self.owner = owner   # ID игрока
        self.is_city = is_city  # Флаг, является ли поселение городом

    def upgrade_to_city(self):
        """Преобразует поселение в город.""" 
        self.is_city = True

    def __repr__(self):
        return "City" if self.is_city else "Settlement"