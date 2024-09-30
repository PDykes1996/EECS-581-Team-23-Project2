from player import Player
from button import Button
import pygame
import sys

class BattleScreen:
    """
        Display the battle screen where players make attacks.

        Args:
        player (int): The current player
        opponent_ships (list): List of opponent's ships
        hits_grid (list): Grid to track hits and misses
        player_ships (list): List of current player's ships

        Returns:
        int: 0 if no winner, or the winning player number
    """
    
    def __init__(self, colors, gameParams):
        self.gameParams = gameParams # pass in game parameters
        self.colors = colors # colors 
        self.special_enabled = False # special move

    def draw_grid(self, gridParams, opponent=False):
        # Extract game parameters
        screen = self.gameParams["screen"]
        font = self.gameParams["font"]
        # Extract grid parameters
        player = gridParams["player"]
        grid_x = gridParams["grid_x"]
        grid_y = gridParams["grid_y"]

        # Draw grid label
        label_text = font.render(gridParams["label"], True, self.colors["BLACK"])
        self.gameParams["screen"].blit(label_text, (grid_x, grid_y - 60))

        # Draw the grid cells
        for i in range(10):
            for j in range(10):
                cell_x = grid_x + i * gridParams["cell_size"] # get cell size for x and y ranges
                cell_y = grid_y + j * gridParams["cell_size"]

                # Draw grid cell and border
                pygame.draw.rect(screen, self.colors["LIGHT_BLUE"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                pygame.draw.rect(screen, self.colors["BLACK"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]), 1)

                # Draw ships and hits for the player's grid
                if not opponent: # if player
                    if any((j, i) in ship['coords'] for ship in gridParams["player"].ships):
                        pygame.draw.rect(screen, self.colors["DARK_GRAY"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                    if (j, i) in [(y, x) for ship in player.sunk_ships for y, x in ship]:
                        pygame.draw.rect(screen, self.colors["RED"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                # Draw hit and miss markers
                if player.hits[j][i] == 'M': # white circle drawn for miss
                    pygame.draw.circle(screen, self.colors["WHITE"], (cell_x + 15, cell_y + 15), 10, 2)
                elif player.hits[j][i] == 'H': # red x drawn for hit
                    pygame.draw.line(screen, self.colors["RED"], (cell_x + 5, cell_y + 5), (cell_x + 25, cell_y + 25), 2)
                    pygame.draw.line(screen, self.colors["RED"], (cell_x + 25, cell_y + 5), (cell_x + 5, cell_y + 25), 2)

    def handle_special(self, event, playerGridParams, opponentGridParams):
        player = playerGridParams["player"]
        opponent = opponentGridParams["player"] #Get player from the grid parameters
        ret = None
        if event.type == pygame.MOUSEBUTTONDOWN: # when mouse is clicked
            x, y = (event.pos[0] - opponentGridParams["grid_x"]) // opponentGridParams["cell_size"], (event.pos[1] - opponentGridParams["grid_y"]) // opponentGridParams["cell_size"]
            if 0 < x < 9 and 0 < y < 9: # make sure shot fits
                player.special_used = True # special can no longer be used anymore
                for i in range(y-1, y+2): # fire at cell below and above
                    for j in range(x-1, x+2): # fire at cells on either side
                        ship = self.get_ship(opponent, j, i)
                        if ship:
                            opponent.hits[i][j] = 'H'  # Mark as hit
                            if self.check_ship_sunk(opponent, ship):
                                opponent.sunk_ships.append(ship['coords'])
                                ret = "Sink!" # ship is sunk
                            elif ret != "Sink!":
                                ret = "Hit!" # mark hits if ship is not sunk
                        else:
                            opponent.hits[i][j] = 'M'  # Mark as miss
                            
                        if ret != "Sink!" and ret != "Hit!":
                            ret = "Miss!" # display miss
            return ret

    def handle_attack(self, event, playerGridParams, opponentGridParams):
        player = playerGridParams["player"]
        if self.special_enabled and not player.special_used:                            #If special is selected and not used yet this game...
            return self.handle_special(event, playerGridParams, opponentGridParams)     #...shoot a special attack

        else:                                                                           #Otherwise continue with the regular attack...                                          
            opponent = opponentGridParams["player"] #Get player from the grid parameters

            if event.type == pygame.MOUSEBUTTONDOWN:                                                                                                                                        # When mouse is clicked...
                x, y = (event.pos[0] - opponentGridParams["grid_x"]) // opponentGridParams["cell_size"], (event.pos[1] - opponentGridParams["grid_y"]) // opponentGridParams["cell_size"]   # ...get the x and y coordinates of the cell clicked...
                if 0 <= x < 10 and 0 <= y < 10:                                                                                                                                             # ...Ensure click is in the grid...
                    if opponent.hits[y][x] is None:                                                                                                                                         # ...Ensure cell has not been attacked...                               
                        ship = self.get_ship(opponent, x, y)                                                                                                                                    # ...Check if there is a ship at the coordinates...             
                        if ship:                                                                                                                                                                    # ...If there is a ship...                                         
                            opponent.hits[y][x] = 'H'                                                                                                                                               # ...Mark as hit
                            if self.check_ship_sunk(opponent, ship):                                                                                                                                    # If entire ship is hit...
                                opponent.sunk_ships.append(ship['coords'])                                                                                                                              # ...mark ship as sunk...                                     
                                return "Sink!"                                                                                                                                                          # ...return that ship is sunk
                            else:                                                                                                                                                                       # Otherwise...
                                return "Hit!"                                                                                                                                                           # ...return that ship is hit
                        else:                                                                                                                                                                       # If there is no ship...                                           
                            opponent.hits[y][x] = 'M'                                                                                                                                               # Mark as miss
                            return "Miss!"                                                                                                                                                          # Return that it is a miss      
                    else:                                                                                                                                                                   # If cell has already been attacked...                     
                        return "Already Attacked!"                                                                                                                                          # ...display as already attacked
            return None                                                                                                                                                                 # Return nothing if no attack is made (Player clicked outside the grid)

    def get_ship(self, opponent, x, y):
        """Find the ship at the given coordinates."""
        for ship in opponent.ships:         # Loop through all ships of opponent...
            if (y, x) in ship['coords']:    # ...if the coordinates are in the ship's coordinates...
                return ship                 # ...return the ship...
        return None                         # ...otherwise, return None if no ship is found

    def check_ship_sunk(self, player, ship): 
        """Check if all coordinates of a ship have been hit."""
        return all(player.hits[y][x] == 'H' for y, x in ship['coords']) # check if all ship coords are hit


    def all_ships_sunk(self, player):
        """Check if all ships of a player have been sunk."""
        return all(self.check_ship_sunk(player, ship) for ship in player.ships) # see if any ships remain
    
    def end_turn(self):
        self.finished = True # turn is finished; moves game to next state

    def toggle_special(self): # toggle special on/off using button
        self.special_enabled = not self.special_enabled

    def display(self, player):
        # Extract game parameters
        screen = self.gameParams["screen"]
        font = self.gameParams["font"] # font from game parameters
        # Determine opponent
        opponent = self.gameParams["player2"] if player.player_id == 1 else self.gameParams["player1"]
        self.finished = False
        attack_made = False # no attacks made yet
        shot_result = None # no shot results yet

        while not self.finished:
            screen.fill(self.colors["WHITE"])  # Clear the screen

            # Display instruction for the current player
            text = font.render(f"Player {player.player_id}: Select a cell to attack", True, self.colors["BLACK"])
            screen.blit(text, (300, 20))


            opponentGridParams ={
                "player" : opponent,
                "label" : "Opponent's Grid", # dimensions for grid
                "grid_x" : 600,
                "grid_y" : 130,
                "cell_size" : 30, # dimensions for cell
                "font_offset_x" : 10,
                "font_offset_y" : 5,
                "line_thickness" : 2, # border settings
                "circle_radius" : 10,
                "special_used": False
            }

            playerGridParams = {
                "player" : player,
                "label" : "Your Grid", # dimensions for grid
                "grid_x" : 50,
                "grid_y" : 130,
                "cell_size" : 30, # dimensions for cell
                "font_offset_x" : 10,
                "font_offset_y" : 5,
                "line_thickness" : 2, # border settings
                "circle_radius" : 10,
                "special_used": False
            }

            # Draw the opponent's grid (for attacks) and player's own grid
            self.draw_grid(opponentGridParams, opponent=True)
            self.draw_grid(playerGridParams)

            if shot_result: # display message for hit, miss, sunk, already attacked
                result_text = font.render(shot_result, True, self.colors["BLACK"])
                screen.blit(result_text, (400, 650))

            # Draw the finish turn button
            finish_turn_buttonParams = {
                "x": 800, # dimensions and location for button
                "y": 600,
                "width": 150,
                "height": 50,
                "action": self.end_turn, # end turn when pressed
                "text": "Finish Turn", # label
                "button_color": self.colors["LIGHT_GRAY"] # color
            }
            finish_turn_button = Button(self.colors, self.gameParams, finish_turn_buttonParams, enabled = attack_made ) # button created
            finish_turn_button.draw() # draw button

            if player.special_used == False:
                # special button
                special_buttonParams = {
                    "x": 600, # dimensions and location for button
                    "y": 600,
                    "width": 170,
                    "height": 50,
                    "action": self.toggle_special, # toggle special shot when pressed
                    "text": "Special Move", # label
                    "button_color": self.colors["RED"] if self.special_enabled else self.colors["LIGHT_GRAY"] # color
                }
                special_button = Button(self.colors, self.gameParams, special_buttonParams) # button created
                special_button.draw() # draw button

            for event in pygame.event.get():    # listen for events...
                if event.type == pygame.QUIT:   # ...if the user closes the window...
                    pygame.quit()               # ...exit program...
                    sys.exit()                  # ...and quit


                if not attack_made:                                                                 # if attack has not been made...
                    shot_result = self.handle_attack(event, playerGridParams, opponentGridParams)   # ...handle the attack...
                    if shot_result:                                                                 # ...if the attack is made...                        
                        attack_made = True                                                          # ...Set attack made to True...

            pygame.display.flip()  # Update the display

            # Check for a winner
            if self.all_ships_sunk(opponent):
                self.finished = True
                self.gameParams["winner"] = player
                return # Return the winning player ID
            if self.finished:
                return 0  # Continue the game