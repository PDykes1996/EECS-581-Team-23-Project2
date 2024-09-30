import random
from enum import Enum
from battle_screen import BattleScreen

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.first_hit = None
        self.previous_hit = None
        self.fire_before = True
        self.horizontal = True
        self.player_id = 2
        self.ships = None
        self.sunk_ships = []
        self.hits = [[None] * 10 for _ in range(10)]
        self.attack_grid = [[None for _ in range(10)] for _ in range(10)]

    def level_one(self, player):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        while player.hits[y][x] != None:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        ship = BattleScreen().get_ship(player, x, y)
        if ship:
            player.hits[y][x] = 'H'  # Mark as hit
            if self.check_ship_sunk(player, ship):
                player.sunk_ships.append(ship['coords'])

        else:
            player.hits[y][x] = 'M'  # Mark as miss


    def level_two(self, player):
        if not self.first_hit:
            self.level_one()

        if not self.previous_hit:
            self.previous_hit = self.first_hit

        if self.horizontal:
            if self.fire_before:
                x, y = self.previous_hit[0] - 1, self.previous_hit[1]

            else:
                x, y = self.previous_hit[0] + 1, self.previous_hit[1]

        else:
            if self.fire_before:
                x, y = self.previous_hit[0], self.previous_hit[1] - 1

            else:
                x, y = self.previous_hit[0], self.previous_hit[1] + 1

        ship = BattleScreen().get_ship(player, x, y)
        if ship:
            self.previous_hit = (x, y)
            player.hits[y][x] = 'H'  # Mark as hit
            if self.check_ship_sunk(player, ship):
                self.first_hit = None
                player.sunk_ships.append(ship['coords'])

        else:
            # fire_before: True
            if self.horizontal and self.fire_before == False:
                self.horizontal = False
            
            else:
                self.fire_before = not self.fire_before
                self.previous_hit = self.first_hit
                player.hits[y][x] = 'M'  # Mark as miss
        

    def level_three(self):
        pass

    def fire(self, player):
        if self.difficulty == 1:
            self.level_one()

        if self.difficulty == 2:
            self.level_two()

        if self.difficulty == 3:
            self.level_three()