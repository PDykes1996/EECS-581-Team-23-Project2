import random
#from battle_screen import BattleScreen

class Player:
    def __init__(self, player_id, difficulty=None):
        self.player_id = player_id #player id
        self.ships = [] #list of ships
        self.sunk_ships = [] #sunk ships list
        self.hits = [[None] * 10 for _ in range(10)] #list comprehension for creating ten element list all elements initialized to None
        self.attack_grid = [[None for _ in range(10)] for _ in range(10)] #same thing as above line
        self.special_used = False #initializing to false, set to true once used, can't use again
        #self.special_enabled = False #same thing
        self.first_hit = None #
        self.previous_hit = None
        self.fire_before = True
        self.horizontal = True
        self.recent_hits = 0

        if difficulty is None:
            self.difficulty = None
            self.isAI = False
        
        else:
            self.difficulty = difficulty
            self.isAI = True

    def get_ship(self, opponent, x, y):
        """Find the ship at the given coordinates."""
        for ship in opponent.ships:
            if (y, x) in ship['coords']:
                return ship
        return None
    
    def check_ship_sunk(self, player, ship):
        """Check if all coordinates of a ship have been hit."""
        return all(player.hits[y][x] == 'H' for y, x in ship['coords'])

    def all_ships_sunk(self, player):
        """Check if all ships of a player have been sunk."""
        return player.ships != [] and all(self.check_ship_sunk(player, ship) for ship in player.ships)
    
    def place_AI_ships(self, num_ships):
        for length in range(1, num_ships + 1):
            # randomly generate a position for a ship
            horizontal = random.choice([True, False])
            if horizontal:
                x = random.randint(0, 10 - length)
                y = random.randint(0, 9)
                print("horizontal ship:")
                print({'coords': set((y, j) for j in range(x, x + length - 1)), 'size': length})
                self.ships.append({'coords': set((y, j) for j in range(x, x + length - 1)), 'size': length})
            else:
                x = random.randint(0, 9)
                y = random.randint(0, 10 - length)
                print("vertical ship:")
                print({'coords': set((i, x) for i in range(y, y + length)), 'size': length})
                self.ships.append({'coords': set((i, x) for i in range(y, y + length)), 'size': length})

    def level_one(self, player):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        while player.hits[y][x] != None:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        ship = self.get_ship(player, x, y)
        if ship:
            player.hits[y][x] = 'H'  # Mark as hit
            if self.check_ship_sunk(player, ship):
                player.sunk_ships.append(ship['coords'])
                return (x, y, 'S')
            else:
                return (x, y, 'H')

        else:
            player.hits[y][x] = 'M'  # Mark as miss
            return (x, y, 'M')


    def level_two(self, player):
        # if ai has not hit ship recently, behave like level_one
        if not self.first_hit:
            result = self.level_one(player)
            if result[2] == 'S':
                self.first_hit = None
                self.previous_hit = None
                self.recent_hits += 1
            elif result[2] == 'H':
                self.first_hit = (result[0], result[1])
                self.recent_hits += 1
            return

        # if previous hit has not been set, but first hit has been set, set previous hit to first hit
        if not self.previous_hit:
            self.previous_hit = self.first_hit

        # if ai is firing horizontally
        if self.horizontal:
            if self.previous_hit[0] <= 0:
                self.fire_before = False
                self.level_two(player)
                return

            # if firing to the left
            print(self.fire_before, player.hits[self.previous_hit[1]][self.previous_hit[0] - 1])
            if self.fire_before and player.hits[self.previous_hit[1]][self.previous_hit[0] - 1] == None:
                # decrement x coordinate by 1 from previous x coordinate
                x, y = self.previous_hit[0] - 1, self.previous_hit[1]
            # otherwise increment x coordinate by 1 from previous x coordinate
            elif self.previous_hit[0] < 9 and player.hits[self.previous_hit[1]][self.previous_hit[0] + 1] == None:
                x, y = self.previous_hit[0] + 1, self.previous_hit[1]


        # if ai is firing vertically
        else:
            if self.previous_hit[1] <= 0:
                self.fire_before = False
                self.level_two(player)

            # if firing above, decrement y coordinate by 1 from previous x coordinate
            if self.fire_before and self.previous_hit[1] > 0 and player.hits[self.previous_hit[1] - 1][self.previous_hit[0]] == None:
                x, y = self.previous_hit[0], self.previous_hit[1] - 1
            # otherwise increment y coordinate by 1 from previous x coordinate
            elif self.previous_hit[1] < 9 and player.hits[self.previous_hit[1] + 1][self.previous_hit[0]] == None:
                x, y = self.previous_hit[0], self.previous_hit[1] + 1

        # get the ship at the coordinates
        ship = self.get_ship(player, x, y)

        # if there is a ship at the coordinates
        if ship:
            self.previous_hit = (x, y)                      # update previous_hit
            player.hits[y][x] = 'H'                         # Mark as hit on player board

            # if ship was sunk
            if self.check_ship_sunk(player, ship):
                self.first_hit = None                       # reset first_hit to None
                self.previous_hit = None
                player.sunk_ships.append(ship['coords'])    # append the sunk ship to the player's sunk_ships

        # if there is no ship at coordinates
        elif self.horizontal:
            if self.fire_before:   # if firing horizontally and firing to the left
                self.fire_before = False    # start firing to the right
            
            # if firing horizontally and firing to the right
            else:
                self.fire_before = True    # reset fire_before
                self.horizontal = False
                if self.recent_hits == 0:
                    self.first_hit = None
                    self.previous_hit = None
                    self.fire_before = True
                    self.horizontal = True
                    self.recent_hits = 0
                
            self.previous_hit = self.first_hit  # set previous hit to the first hit
            self.hits[y][x] = 'M'  # Mark as miss

        elif self.fire_before:   # if firing horizontally and firing to the left
            self.fire_before = False    # start firing to the right 
            self.previous_hit = self.first_hit  # set previous hit to the first hit
            self.hits[y][x] = 'M'  # Mark as miss
            if self.recent_hits:
                    self.first_hit = None
                    self.previous_hit = None
                    self.fire_before = True
                    self.horizontal = True
                    self.recent_hits = 0


    def level_three(self, player):
        found_ship = False
        for ship in player.ships:
            if not self.check_ship_sunk(player, ship):
                found_ship = True
                for i, j in ship["coords"]:
                    if player.hits[i][j] is None:
                        y = i
                        x = j
                        ship = self.get_ship(player, x, y)
                        if ship:
                            player.hits[y][x] = 'H'  # Mark as hit
                            if self.check_ship_sunk(player, ship):
                                player.sunk_ships.append(ship['coords'])

                        else:
                            player.hits[y][x] = 'M'  # Mark as miss
                        break
            if found_ship == True:
                break


    def fire(self, player):
        if self.difficulty == "Easy":
            self.level_one(player)

        if self.difficulty == "Medium":
            self.level_two(player)

        if self.difficulty == "Hard":
            self.level_three(player)

        if self.all_ships_sunk(player):
            #self.finished = True
            return self
            #return # Return the winning player ID
        #if self.finished:
            #return 0  # Continue the game