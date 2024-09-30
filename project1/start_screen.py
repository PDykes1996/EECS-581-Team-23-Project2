import pygame
import sys
from button import Button

class StartScreen:
    def __init__(self, gameParams, colorDict):
        self.colors = colorDict
        self.gameParams = gameParams
        self.play_mode_selected = False  # Indicates if Player vs AI or Player vs Player mode has been selected
        self.ai_mode = None  # Tracks if AI mode is selected
        self.difficulty_selected = None  # Tracks if AI difficulty has been selected
        self.ship_selection_active = False  # Controls when to display ship selection

    def display(self):
        """
        Display the start screen where players select the game mode, AI difficulty (if applicable), and number of ships.
        """

        while self.gameParams["num_ships"] == 0:  # loop until the number of ships is selected
            self.gameParams["screen"].fill(self.colors["WHITE"])  # clear the screen with a white background

            # first choose between player vs player or player vs ai
            if not self.play_mode_selected:
                self.display_mode_selection()
            # if ai is chosen display AI difficulty selection
            elif self.ai_mode and not self.difficulty_selected:
                self.display_ai_difficulty_selection()
            # when both mode and difficulty (if AI) are selected display ship selection
            else:
                self.display_ship_selection()

            # handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # quit pygame
                    sys.exit() # quit program

            pygame.display.flip()  # update the display

    def display_mode_selection(self):
        """
        Display the screen where the player selects whether to play against another player or AI.
        """
        # display screen to select gamemode
        text = self.gameParams["font"].render("Select Game Mode:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100))

        # button parameters for PvP gamemode (selects mode to vs another player)
        player_button_params = {
            "x": 300, "y": 200, "width": 200, "height": 50, # dimensions for button
            "button_color": self.colors["LIGHT_GRAY"], "action": self.select_player_mode, "text": "Player vs Player" # button color, action, and label
        }
        # button paramters for PvAI gamemode (selects mode to vs AI bot)
        ai_button_params = {
            "x": 300, "y": 300, "width": 200, "height": 50, # dimensions for button
            "button_color": self.colors["LIGHT_GRAY"], "action": self.select_ai_mode, "text": "Player vs AI" # color, action, label
        }

        # create button using parameters listed above (one for pvp and one for ai)
        playerButton = Button(self.colors, self.gameParams, player_button_params) # PvP button created
        aiButton = Button(self.colors, self.gameParams, ai_button_params) #PvAI button created

        # draw the buttons on the screen
        playerButton.draw() # PvP
        aiButton.draw() # PvAI

    def select_player_mode(self):
        """Set the game mode to Player vs Player."""
        self.play_mode_selected = True # store the fact that the game mode has been selected
        self.ship_selection_active = True  # continues game to ship selection after this

    def select_ai_mode(self):
        """Set the game mode to Player vs AI and proceed to difficulty selection."""
        self.play_mode_selected = True # store the fact that the game mode has been selected
        self.ai_mode = True  # AI mode selected
        self.ship_selection_active = False  # prevent ship selection until difficulty is chosen
        self.gameParams["player2"].isAI = True

    def display_ai_difficulty_selection(self):
        """
        Display the screen where the player selects AI difficulty.
        """
        # organize screen to display select ai difficulty
        text = self.gameParams["font"].render("Select AI Difficulty:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100)) # screen with text is displayed

        # parameters for easy mode button
        easy_button_params = {
            "x": 300, "y": 175, "width": 200, "height": 50, # dimensions for button
            "action": lambda: self.set_difficulty("Easy"), "text": "Easy", "button_color": self.colors["LIGHT_GRAY"] # color, action, label
        }
        medium_button_params = {
            "x": 300, "y": 350, "width": 200, "height": 50, # dimensions for button
            "action": lambda: self.set_difficulty("Medium"), "text": "Medium", "button_color": self.colors["LIGHT_GRAY"] # color, action, label
        }
        hard_button_params = {
            "x": 300, "y": 525, "width": 200, "height": 50, # dimensions for button
            "action": lambda: self.set_difficulty("Hard"), "text": "Hard", "button_color": self.colors["LIGHT_GRAY"] # color, action, label
        }

        easyButton = Button(self.colors, self.gameParams, easy_button_params) # easy button created 
        mediumButton = Button(self.colors, self.gameParams, medium_button_params) # medium button created
        hardButton = Button(self.colors, self.gameParams, hard_button_params) # hard button created

        easyButton.draw() # buttons drawn on screen
        mediumButton.draw()
        hardButton.draw()

    def set_difficulty(self, difficulty):
        # Set the AI difficulty and proceed to ship selection.
        self.gameParams["ai_difficulty"] = difficulty # ai difficulty is passed into parameters
        self.difficulty_selected = True # imply that difficulty has been selected
        self.ship_selection_active = True # and signal that ship selection is ready
        self.gameParams["player2"].difficulty = difficulty

    """
    def set_difficulty(self, difficulty):
        #Set the AI difficulty and proceed to ship selection.
        self.gameParams["ai_difficulty"] = difficulty
        self.difficulty_selected = True
        self.ship_selection_active = True  # Now allow ship selection after difficulty
    """

    def display_ship_selection(self):
        """
        Display the screen where players select the number of ships to play with.
        """
        # screen to display ships number selection established
        text = self.gameParams["font"].render("Select number of ships to play with:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100))

        # Create buttons for ship selection (1 to 5 ships)
        for i in range(1, 6): # loop until 5 total buttons
            ship_num_buttonParams = {
                "x": int(150 + 100 * i), # dimensions for buttons
                "y": 250,
                "width": 80,
                "height": 50,
                "button_color": self.colors["LIGHT_GRAY"], # color
                "action": lambda i=i: self.set_num_ships(i), # set ship_num to whatever respective button is clicked
                "text": str(i) # display numbers 1-5 on buttons
            }
            numSelector = Button(self.colors, self.gameParams, ship_num_buttonParams) # buttons created
            numSelector.draw() # buttons drawn on screen

    def set_num_ships(self, num):
        """Set the number of ships for the game."""
        self.gameParams["num_ships"] = num
        # After ship selection, you can move to the next phase of the game