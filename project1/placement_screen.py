import pygame
import sys
from player import Player
from button import Button

class PlacementScreen:
    def __init__(self, colors, gameParams):
        """
        colors (dict): A dictionary containing color names as keys and RGB tuples as values.
        {
            "WHITE"
            "BLACK"
            "LIGHT_GRAY"
            "DARK_GRAY" 
            "LIGHT_BLUE" 
            "RED" 
            "GRID_BLUE"
        }
        gameParams (dict): A dictionary containing game parameters.
        {
            "winner" : Boolean, Indicates if there is a winner
            "game_running": Boolean, True while game running
            "restart_game": Boolean, True if game is to be restarted
            "num_ships": (int), Number of ships to place
            "player1" : (Player), Player 1 object
            "player2" : (Player), Player 2 object. Can be AI or human
            "screen" : Game Window
            "font" : Default font for text
            "special_enabled": False
        }
        """
        self.colors = colors
        self.gameParams = gameParams

    def display(self, player):
        """
        Display the ship placement screen for a player.

        Args:
        player (int): The player number (1 or 2)
        """
        # Initialize empty grid and ships for placement
        grid = [[None] * 10 for _ in range(10)]                                                                 #initially 10x10 grid is empty
        ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(self.gameParams["num_ships"])] #ships start off the grid
        self.selected = None                                                                                    # Currently selected ship
        self.vertical = False                                                                                   # Ship orientation (horizontal by default)
        self.finished = False                                                                                   # Flag to track when placement is complete

        while not self.finished:
            self.gameParams["screen"].fill(self.colors["WHITE"])                    # Clear screen
            self._draw_text(f"Player {player.player_id} Ship Placement", (350, 20)) # Display player instructions
            self._draw_grid(grid)                                                   # Draw the placement grid
            self._draw_ships(ships)                                                 # Draw the ships in the side panel
            

            # Button Parameters
            rotateButton = Button(
                self.colors, self.gameParams,
                {"x": 600,                                                  # Button Coordinates
                 "y": 600, 
                 "width": 150,                                              # Button Dimensions               
                 "height": 50, 
                 "button_color": self.colors["LIGHT_GRAY"],                 # Button Color
                 "action": None,                                            # Action when button clicked
                 "text": "Rotate (V)" if self.vertical else "Rotate (H)"}   # Text on the button
            )
            finishButton = Button(
                self.colors, self.gameParams,
                {"x": 800,                                  # Button Coordinates
                 "y": 600, 
                 "width": 150,                              # Button Dimensions
                 "height": 50, 
                 "button_color": self.colors["LIGHT_GRAY"], # Button Color
                 "action": None,                            # Action when button clicked
                 "text": "Finish"}                          # Text on the button
            )

            rotateButton.draw() #Draw rotate button
            finishButton.draw() #Draw finish button

            # Show placement indicator
            mouse_pos = pygame.mouse.get_pos()
            if self.selected is not None:
                self._draw_placement_indicator(ships[self.selected], mouse_pos, self.vertical)

            # Handle user inputs
            self._handle_events(ships, grid)

            # Update the display
            pygame.display.flip()

        # Store the placed ships for each player
        self._store_ships(player.player_id, grid)

    def _draw_text(self, text, pos):
        """Helper function to render and display text."""
        rendered_text = self.gameParams["font"].render(text, True, self.colors["BLACK"])
        self.gameParams["screen"].blit(rendered_text, pos)

    def _draw_grid(self, grid):
        """Helper function to draw the placement grid."""
        for i in range(10):     #Columns of grid
            for j in range(10): #Rows of grid
                rect = pygame.Rect(50 + i * 50, 100 + j * 50, 50, 50)                       #creating rectangle for each position of grid
                pygame.draw.rect(self.gameParams["screen"], self.colors["GRID_BLUE"], rect) #draw in blue grid square background
                pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], rect, 1)  #outline each grid square in black

                if grid[j][i] is not None:                                                      #If ship part present at this grid pos...
                    pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], rect) #...draw in dark grey to indicae ship

                # Draw grid labels (A-J, 1-10)
                self._draw_text(chr(65 + i), (65 + i * 50, 70))
                self._draw_text(str(j + 1), (20, 115 + j * 50))

    def _draw_ships(self, ships):
        """Helper function to draw ships in the side panel."""
        for i, ship in enumerate(ships):                                               #For each ship...
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], ship)#...Change the color of it's grid square to dark grey

            if i == self.selected:                                                      #If ship is currently selected...
                pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], ship, 2)#...draw a red outline around it

    def _draw_placement_indicator(self, ship, mouse_pos, vertical):
        """Draw a placement indicator for the selected ship."""
        size = max(ship.width, ship.height) // 50 #ship size being determined in grid cells
        if vertical:                                                                        #If ship is vertical...
            indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size * 50)    #...draw a vertical ship indicator around mouse pos

        else:                                                                               #If ship is horizontal...
            indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size * 50, 50)    #...draw a horizontal ship indicator around mouse pos

        pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], indicator, 2)       #Draw a red outline around currently selected ship

    def _toggle_orientation(self):
        """Toggle ship orientation."""
        self.vertical = not self.vertical #Togggle between veritcal and not vertical (horizontal)

    def _finish_placement(self, ships):
        """Finish ship placement if all ships are placed."""
        all_ships_placed = all(ship.left < 600 for ship in ships)#Return True if all ships are placed on the grid
        if all_ships_placed:     #If all ships placed...
            self.finished = True #...set finished parameter to true, allows for game to start

    def _handle_events(self, ships, grid):
        """Handle user input events."""
        for event in pygame.event.get(): #loop through all the events tha can occur
            if event.type == pygame.QUIT: #if close button clicked
                pygame.quit() #quit the game
                sys.exit() #exit
            if event.type == pygame.KEYDOWN: #h key allows for horizontal placement
                if event.key == pygame.K_h: #if h clicked
                    self.vertical = False #vertical will change to false
                elif event.key == pygame.K_v: #same logic but for other key
                    self.vertical = True #using true not changing it to if v clicked make horizontal false, easier implementation
            if event.type == pygame.MOUSEBUTTONDOWN: #pass to mouse handler
                self._handle_mouse_click(event, ships, grid) #processing ship placement here

    def _handle_mouse_click(self, event, ships, grid):
        """Handle mouse clicks for ship placement and selection."""
        mouse_pos = event.pos #get current mouse position

        # Handle button clicks for rotate and finish
        rotateButtonRect = pygame.Rect(600, 600, 150, 50) #button to rotate
        finishButtonRect = pygame.Rect(800, 600, 150, 50) #button to finalize placement

        all_ships_placed = all(ship.left < 600 for ship in ships) #ensuring number of ships selected have all been placed

        if rotateButtonRect.collidepoint(mouse_pos): #if mouse click on rotate button
            self._toggle_orientation() #switch the orientation from vertical to horizontal or other way around
            return  # Exit early since we've handled the click
        elif finishButtonRect.collidepoint(mouse_pos) and all_ships_placed: #if finish button clicked
            self._finish_placement(ships) #finalize placement
            return  # Exit early since we've handled the click

        x, y = (mouse_pos[0] - 50) // 50, (mouse_pos[1] - 100) // 50 #figuring out grid coordinate mouse is on
        if 0 <= x < 10 and 0 <= y < 10: #click has to be within bounds
            if self.selected is not None: #if there is a ship currently selected
                size = max(ships[self.selected].width, ships[self.selected].height) // 50 #figure out the size of the ship, whichever is greater between width or height
                if self.is_valid_placement(x, y, size, self.vertical, self.selected + 1, grid): #if all parameters line up for valud placement
                    self.clear_ship(self.selected + 1, grid)  # Clear old position of the ship

                    # Place the ship on the grid based on orientation
                    for i in range(size):
                        if self.vertical:
                            grid[y + i][x] = self.selected + 1  # Place ship vertically
                        else:
                            grid[y][x + i] = self.selected + 1  # Place ship horizontally

                    # Update ship position in the 'ships' list with correct orientation
                    ships[self.selected] = pygame.Rect(
                        50 + x * 50, 100 + y * 50,
                        50 if self.vertical else size * 50, #adjust width based on orientation of page
                        size * 50 if self.vertical else 50 #same for height
                    )
                    self.selected = None  # Deselect the ship after placing it

            else:
                # Clicking on the grid without a selected ship does nothing
                pass
        else:
            # Select a ship from the side panel, checking because this is a button click outside of the grid
            for i, ship in enumerate(ships): #if mouse click inside a rectangle of side panel ship
                if ship.collidepoint(mouse_pos): #select the ship being selected
                    self.selected = i #store it
                    self.clear_ship(i + 1, grid) #clear previous placement of that ship if there was one
                    break

    def clear_ship(self, ship_num, grid):
        """Remove a ship from the grid."""
        for y in range(10): #nested for loops for location
            for x in range(10): #now for x coordinate
                if grid[y][x] == ship_num: #if the ship wanting ot be cleared overlaps this coordinate
                    grid[y][x] = None #set it to None

    def is_valid_placement(self, x, y, size, is_vertical, ship_num, grid):
        """Check if a ship placement is valid."""
        # Check if ship is within grid bounds
        if is_vertical and y + size > 10: #limit is 10x10 grid
            return False #can't do it
        if not is_vertical and x + size > 10: #same thing for other axis
            return False

        # Check for overlap with other ships
        for i in range(size): #using for loop to iterate through every cell in ship (its size)
            check_x = x + (0 if is_vertical else i) #we are trying ot figire out x coordinate,
            check_y = y + (i if is_vertical else 0) #figuring out y coordinate

            if grid[check_y][check_x] is not None and grid[check_y][check_x] != ship_num: #here we check if another ship is overlapping the square occupied by existing ship
                return False

        return True #if passes without returning false, return true, allow placement

    def _store_ships(self, player, grid):
        """Store the placed ships in the game parameters."""
        if player == 1: #check if player 1 is player 1
            #storing ships for player 1 in game params dict using key 'player1'
            self.gameParams["player1"].ships = [
                #storing set of all the coordinates where ships are placed
                {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in range(self.gameParams["num_ships"])
            ]
        else:
            #same stuff as above but for player 2
            self.gameParams["player2"].ships = [
                {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in range(self.gameParams["num_ships"])
            ]       