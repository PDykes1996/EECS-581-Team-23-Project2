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
        self.special_enabled = False #same thing
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
        ship_sizes = list(range(1, num_ships + 1))
        placed_ships = []


        for length in ship_sizes:
            valid_position = False

            # Try placing the ship until a valid position is found
            while not valid_position:
                horizontal = random.choice([True, False])  # Randomly choose orientation
                if horizontal:
                    x = random.randint(0, 10 - length)  # Ensure ship fits horizontally
                    y = random.randint(0, 9)            # Vertical position
                else:
                    x = random.randint(0, 9)            # Horizontal position
                    y = random.randint(0, 10 - length)  # Ensure ship fits vertically

                # Generate ship coordinates based on orientation
                if horizontal:
                    new_ship_coords = {(y, i) for i in range(x, x + length)}
                else:
                    new_ship_coords = {(i, x) for i in range(y, y + length)}

                # Check if the new ship overlaps with any previously placed ship
                if not any(coord in placed_ship['coords'] for placed_ship in self.ships for coord in new_ship_coords):
                    # No overlap found, so place the ship
                    self.ships.append({'coords': new_ship_coords, 'size': length})
                    placed_ships.append({'coords': new_ship_coords, 'size': length})
                    valid_position = True

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
        # if AI has not hit a ship recently, behave like level_one
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

        while True:
            # If firing horizontally
            if self.horizontal:
                # If at the edge of the grid, switch direction
                if self.previous_hit[0] <= 0:
                    self.fire_before = False

                # If firing to the left
                if self.fire_before and self.previous_hit[0] > 0 and player.hits[self.previous_hit[1]][self.previous_hit[0] - 1] is None:
                    x, y = self.previous_hit[0] - 1, self.previous_hit[1]
                # Otherwise, fire to the right
                elif self.previous_hit[0] < 9 and player.hits[self.previous_hit[1]][self.previous_hit[0] + 1] is None:
                    x, y = self.previous_hit[0] + 1, self.previous_hit[1]
                else:
                    # Switch to vertical if both horizontal directions are exhausted
                    self.horizontal = False
                    continue

            # If firing vertically
            else:
                # If at the edge of the grid, switch direction
                if self.previous_hit[1] <= 0:
                    self.fire_before = False

                # If firing above
                if self.fire_before and self.previous_hit[1] > 0 and player.hits[self.previous_hit[1] - 1][self.previous_hit[0]] is None:
                    x, y = self.previous_hit[0], self.previous_hit[1] - 1
                # Otherwise, fire below
                elif self.previous_hit[1] < 9 and player.hits[self.previous_hit[1] + 1][self.previous_hit[0]] is None:
                    x, y = self.previous_hit[0], self.previous_hit[1] + 1
                else:
                    # Reset AI state if all directions are exhausted
                    self.first_hit = None
                    self.previous_hit = None
                    self.fire_before = True
                    self.horizontal = True
                    self.recent_hits = 0
                    return

            # Get the ship at the coordinates
            ship = self.get_ship(player, x, y)

            # If there is a ship at the coordinates
            if ship:
                self.previous_hit = (x, y)  # Update previous_hit
                player.hits[y][x] = 'H'  # Mark as hit on the player's board

                # If the ship was sunk
                if self.check_ship_sunk(player, ship):
                    self.first_hit = None  # Reset first_hit
                    self.previous_hit = None
                    player.sunk_ships.append(ship['coords'])  # Append the sunk ship to the player's sunk_ships
                return

            # If there is no ship at the coordinates
            else:
                player.hits[y][x] = 'M'  # Mark as miss

                # If firing horizontally and hit a miss
                if self.horizontal:
                    if self.fire_before:  # If firing left, switch to firing right
                        self.fire_before = False
                    else:  # If firing right, switch to vertical
                        self.horizontal = False
                else:
                    # If vertical direction was exhausted, reset the AI's firing pattern
                    self.first_hit = None
                    self.previous_hit = None
                    self.fire_before = True
                    self.horizontal = True
                    self.recent_hits = 0
                return


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