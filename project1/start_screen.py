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

        while self.gameParams["num_ships"] == 0:  # Loop until the number of ships is selected
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear the screen with a white background

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
                    pygame.quit() # quit this page
                    sys.exit() # 

            pygame.display.flip()  # update the display

    def display_mode_selection(self):
        """
        Display the screen where the player selects whether to play against another player or AI.
        """
        text = self.gameParams["font"].render("Select Game Mode:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100))

        player_button_params = {
            "x": 300, "y": 200, "width": 200, "height": 50,
            "button_color": self.colors["LIGHT_GRAY"], "action": self.select_player_mode, "text": "Player vs Player"
        }
        ai_button_params = {
            "x": 300, "y": 300, "width": 200, "height": 50,
            "button_color": self.colors["LIGHT_GRAY"], "action": self.select_ai_mode, "text": "Player vs AI"
        }

        playerButton = Button(self.colors, self.gameParams, player_button_params)
        aiButton = Button(self.colors, self.gameParams, ai_button_params)

        playerButton.draw()
        aiButton.draw()

    def select_player_mode(self):
        """Set the game mode to Player vs Player."""
        self.play_mode_selected = True
        self.ship_selection_active = True  # Allow ship selection after this

    def select_ai_mode(self):
        """Set the game mode to Player vs AI and proceed to difficulty selection."""
        self.play_mode_selected = True
        self.ai_mode = True  # AI mode selected
        self.ship_selection_active = False  # Prevent ship selection until difficulty is chosen

    def display_ai_difficulty_selection(self):
        """
        Display the screen where the player selects AI difficulty.
        """
        text = self.gameParams["font"].render("Select AI Difficulty:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100))

        easy_button_params = {
            "x": 300, "y": 200, "width": 200, "height": 50,
            "action": self.set_easy, "text": "Easy", "button_color": self.colors["LIGHT_GRAY"]
        }
        medium_button_params = {
            "x": 300, "y": 350, "width": 200, "height": 50,
            "action": self.set_medium, "text": "Medium", "button_color": self.colors["LIGHT_GRAY"],
        }
        hard_button_params = {
            "x": 300, "y": 500, "width": 200, "height": 50,
            "action": self.set_hard, "text": "Hard", "button_color": self.colors["LIGHT_GRAY"]
        }

        easyButton = Button(self.colors, self.gameParams, easy_button_params)
        mediumButton = Button(self.colors, self.gameParams, medium_button_params)
        hardButton = Button(self.colors, self.gameParams, hard_button_params)

        easyButton.draw()
        mediumButton.draw()
        hardButton.draw()

    def set_easy(self):
        self.gameParams["ai_difficulty"] = "Easy"
        self.difficulty_selected = True
        self.ship_selection_active = True  # Now allow ship selection after difficulty

    def set_medium(self):
        self.gameParams["ai_difficulty"] = "Medium"
        self.difficulty_selected = True
        self.ship_selection_active = True  # Now allow ship selection after difficulty

    def set_hard(self):
        self.gameParams["ai_difficulty"] = "Hard"
        self.difficulty_selected = True
        self.ship_selection_active = True  # Now allow ship selection after difficulty

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
        text = self.gameParams["font"].render("Select number of ships to play with:", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (250, 100))

        # Create buttons for ship selection (1 to 5 ships)
        for i in range(1, 6):
            ship_num_buttonParams = {
                "x": int(150 + 100 * i),
                "y": 250,
                "width": 80,
                "height": 50,
                "button_color": self.colors["LIGHT_GRAY"],
                "action": lambda i=i: self.set_num_ships(i),
                "text": str(i),
            }
            numSelector = Button(self.colors, self.gameParams, ship_num_buttonParams)
            numSelector.draw()

    def set_num_ships(self, num):
        """Set the number of ships for the game."""
        self.gameParams["num_ships"] = num
        # After ship selection, you can move to the next phase of the game
