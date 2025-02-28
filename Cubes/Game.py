import random


class Game:
    def __init__(self, hparam: int, max_gamers: int, users: []):
        self.id = 0
        self.hparam = hparam
        self.max_gamers = max_gamers
        # self.users = users
        self.gamers = []
        for usr in users:
            gamer_object = {
                "uuid": usr["user_uuid"],
                "login": usr["user_login"],
                "score": 0
            }
            self.gamers.append(gamer_object)
        self.current_player_moving = None
        self.isStarted = False

    # def add_user(self, user_uuid):
    #     # AUser = (message["login"], message["user_uuid"], websocket)
    #     # self.login_users.append(AUser)
    #     if user_uuid not in self.users:
    #         if len(self.users) < self.max_gamers:
    #             self.users.append(user_uuid)

    def start_game(self):
        self.isStarted = True
        print(f"self.gamers: {self.gamers}")

        # while not self.is_game_over():
        #     for gamer in self.gamers:



    def is_game_over(self):
        for gamer in self.gamers:
            if gamer["score"] == 1000:
                return True

        return False

    def roll_dice(self, dice_count: int):
        result = []
        dice = 0
        while dice < dice_count:
            dice_res = random.randint(1, 6)
            print(dice_res)
            Adice = (dice, dice_res)
            result.append(Adice)
            dice = dice + 1
        return result



