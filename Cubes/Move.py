import random
import sys
from collections import Counter


class Move:
    def __init__(self, free_cubes: int):
        self.free_cubes = free_cubes

    def roll_dice(self, dice_count: int):
        result = []
        dice = 0
        while dice < dice_count:
            dice_res = random.randint(1, 6)
            sys.stdout.write(f"{dice_res} \n")
            sys.stdout.flush()
            Adice = (dice, dice_res)
            result.append(dice_res)
            dice = dice + 1
        return result

    def get_combination(self, dices: []):

        # dices = [2, 3, 4, 5, 6]

        counts =  Counter(dices)
        score = 0

        if len(dices) == len(set(dices)):
            if (min(dices) == 1) and (sum(dices) == 15):
                score += 125
                sys.stdout.write(f"  Score: {score} \n")
                sys.stdout.flush()
                return score
            if (min(dices) == 2) and (sum(dices) == 20):
                score += 250
                sys.stdout.write(f"  Score: {score}\n")
                sys.stdout.flush()
                return score


        for num in range(1, 7):
            if counts[num] == 5:
                if num == 1:
                    score += 1000
                else:
                    score += num * 50
                counts[num] -= 5

            if counts[num] == 4:
                if num == 1:
                    score += 200
                else:
                    score += num * 20
                counts[num] -= 4

            if counts[num] == 3:
                if num == 1:
                    score += 100  # Три единицы
                else:
                    score += num * 10   # Три двойки, тройки и т.д.
                counts[num] -= 3        # Убираем использованные кубики

            # Проверяем единицы и пятёрки
        score += counts[1] * 10  # Каждая единица
        score += counts[5] * 5  # Каждая пятёрка

        sys.stdout.write(f"  Score: {score} \n")
        sys.stdout.flush()
        return score


        # # "1" "1" "1" "1" "1" - 1000
        # if all(flag == 1 for (__, flag) in dices):
        #     print("all flag = 1")
        #     return 1000
        #
        # for dice in dices:
        #     pass
        #
        # # "1" "1" "1" "1" "1" - 1000
        # if all(flag == 1 for (__, flag) in dices):
        #     print("all flag = 1")
        #
        # if (1 == 3):
        #     pass
        # else:
        #     print("ELSE")

    def move(self):
        dices = self.roll_dice(5)
        self.get_combination(dices)
