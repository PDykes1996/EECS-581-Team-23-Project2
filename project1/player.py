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
        self.first_hit = None #initialzing
        self.previous_hit = None #initializing
        self.fire_before = True ##initializing
        self.horizontal = True #initializnig
        self.recent_hits = 0 #initializing

        if difficulty is None: #difficult only matters if player2 is set to AI
            self.difficulty = None #need to pass None
            self.isAI = False #set to false
        
        else:
            self.difficulty = difficulty #'Easy', 'Medium', or 'Hard'
            self.isAI = True #envoke ai mode

    def get_ship(self, opponent, x, y):
        """Find the ship at the given coordinates."""
        for ship in opponent.ships: #just finding all the opponent ship, looping through
            if (y, x) in ship['coords']: #returning dictionary as lists of tuples for points checked against ship's current coordinates
                return ship #return
        return None #no ship found at coordinate return None
    
    def check_ship_sunk(self, player, ship):
        """Check if all coordinates of a ship have been hit."""
        return all(player.hits[y][x] == 'H' for y, x in ship['coords']) #loops through list of tuples, 

    def all_ships_sunk(self, player):
        """Check if all ships of a player have been sunk."""
        return player.ships != [] and all(self.check_ship_sunk(player, ship) for ship in player.ships)
    
    def place_AI_ships(self, num_ships):
        for length in range(1, num_ships + 1): #looping thorugh num of ships
            placed = False #flag indicating if current ship has been placed or not
            while not placed: #while loop
                horizontal = random.choice([True, False]) #ai will randomize orientation
                if horizontal: #if horizontal chosen, need to ensure it fits where random location is
                    x = random.randint(0, 10 - length)  # Ensure the ship fits horizontally
                    y = random.randint(0, 9) #same as above line
                    new_ship_coords = set((x + i, y) for i in range(length)) #moving onto generating coords for next ship
                else:
                    x = random.randint(0, 9) #same but for vertical not
                    y = random.randint(0, 10 - length)  # Ensure the ship fits vertically
                    new_ship_coords = set((x, y + i) for i in range(length)) #new ship generated with coords

                # Check if the ship overlaps with any existing ships
                if not any(coord in placed_ship['coords'] for placed_ship in self.ships for coord in new_ship_coords): #if no overlap, add new_ship to list of exising ship coords
                    self.ships.append({'coords': new_ship_coords, 'size': length}) #append it
                    placed = True #flag true for valid placement

    def level_one(self, player):
        #randomizing shots with basic functionality
        x = random.randint(0, 9) #random legal coordinate
        y = random.randint(0, 9) #random legal coordinate

        while player.hits[y][x] != None: #while a selection to shoot at is made by the other player and sent
            x = random.randint(0, 9) #keep generating
            y = random.randint(0, 9) #keep generating

        ship = self.get_ship(player, x, y) #get ship func retrieval to reference against
        if ship: #if ship found
            player.hits[y][x] = 'H'  # Mark as hit
            if self.check_ship_sunk(player, ship): #running check sunk func
                player.sunk_ships.append(ship['coords']) #add to dict list of sunk to display ship sunk
                return (x, y, 'S') #returning coordinate with sunk paramter attached
            else:
                return (x, y, 'H') #if only hit not sunk, make it H param

        else:
            player.hits[y][x] = 'M'  # Mark as miss
            return (x, y, 'M') #retirn M param w coords


    def level_two(self, player):
        # if AI has not hit a ship recently, behave like level_one
        if not self.first_hit: #no hit detected
            result = self.level_one(player) #level one play
            if result[2] == 'S': #if sunk, reset ai tracking alg
                self.first_hit = None #rest
                self.previous_hit = None #rest
                self.recent_hits += 1 #increment
            elif result[2] == 'H': #if only hit
                self.first_hit = (result[0], result[1]) #storing x, y coords x is 0 y is 1
                self.recent_hits += 1 #increment
            return

        # if previous hit has not been set, but first hit has been set, set previous hit to first hit
        if not self.previous_hit: #if hit made but no previous hit set
            self.previous_hit = self.first_hit #linked list functionality, set previous hit to first hit

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
        #hardest level, you will lose unless you somehow hit ten straight shots
        found_ship = False #initializing flag for if ai found ship
        for ship in player.ships: #going through list of tuples of known coordinates for player1 placed ships
            if not self.check_ship_sunk(player, ship): #if ship hasnt been sunk
                found_ship = True #ships still alive, but its been found
                for i, j in ship["coords"]: #iterating over current ship coords
                    if player.hits[i][j] is None: #seting x, y vals to current coords
                        y = i #here
                        x = j #and here
                        ship = self.get_ship(player, x, y) #using ship.get_ship method to find ships
                        if ship: #if coords is a ship
                            player.hits[y][x] = 'H'  # Mark as hit
                            if self.check_ship_sunk(player, ship): #if check sunk method comes back sunk
                                player.sunk_ships.append(ship['coords']) #add these coordinates to sunk ship list

                        else:
                            player.hits[y][x] = 'M'  # Mark as miss
                        break
            if found_ship == True:
                break


    def fire(self, player):
        if self.difficulty == "Easy": #choosing difficult mode
            self.level_one(player) #func level_one, this is the AI player, non AI players cannot have a difficulty

        if self.difficulty == "Medium": #same as above medium level
            self.level_two(player)

        if self.difficulty == "Hard": #same as above hard level
            self.level_three(player)

        if self.all_ships_sunk(player):
            #self.finished = True
            return self
            #return # Return the winning player ID
        #if self.finished:
            #return 0  # Continue the game