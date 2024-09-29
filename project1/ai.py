import random

class AI:
    def __init__(self, gameParams):
        self.difficulty = None
        self.previous_hits = []
        self.gameParams = gameParams

    def level_one(self):
        player = self.gameParams["player1"]
        while player.hits[y][x] is not None:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        return (x, y)
    
    def level_two(self):
        player = self.gameParams["player1"]
        while player.hits[y][x] is not None:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        return (x, y)
    
    def level_three(self):
        player = self.gameParams["player1"]
        if self.previous_hits == []:
            return self.level_one()
        
        else:
            #do something
            pass

    def fire(self):
        player = self.gameParams["player1"]

        if self.diffuclty == 1:
            coords = self.level_one()
        if self.difficulty == 2:
            coords = self.level_two()
        if self.difficulty == 3:
            coords = self.level_three()
        else:
            coords = None


        ship = self.get_ship(player, x, y)
        if ship:
            player[y][x] = 'H'  # Mark as hit
            if self.check_ship_sunk(player, ship):
                player.sunk_ships.append(ship['coords'])
                return "Sink!"
            else:
                return "Hit!"
        else:
            player.hits[y][x] = 'M'  # Mark as miss
            return "Miss!"

            # perform check to make sure AI has not fired

        if self.difficulty == 2:
            pass

        if self.difficulty == 3:
            pass