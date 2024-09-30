import pygame
import sys
from player import Player
from button import Button

class WinScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors # Dictionary of colors 
        self.gameParams = gameParams # Dictionary of game parameters
    
    def new_game(self):
        self.gameParams["restart_game"] = True # Set restart_game to True to start a new game

    def end_game(self):
        self.gameParams["game_running"] = False # Set game_running to False to end the game

    def display(self, player):
        """
        Display the winner screen and options for a new game or to end the game.

        Args:
        player (int): The winning player number
        """
        self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen
        # Display winner text
        text = self.gameParams["font"].render(f"Player {player.player_id} Wins!", True, self.colors["BLACK"]) # Create text surface
        self.gameParams["screen"].blit(text, (380, 200)) # Display text

    # Draw new game and end game buttons
        newGameButtonParams = {
            "x": 300, # x-coordinate of the button
            "y": 400, # y-coordinate of the button
            "width": 150, # width of the button
            "height": 50, # height of the button
            "button_color": self.colors["LIGHT_GRAY"], # color of the button
            "action": self.new_game, # action to perform when the button is clicked
            "text": "New Game" # text to display on the button
        }
        endGameButtonParams = {
            "x": 500, # x-coordinate of the button
            "y": 400, # y-coordinate of the button
            "width": 150, # width of the button
            "height": 50, # height of the button
            "button_color": self.colors["LIGHT_GRAY"], # color of the button
            "action": self.end_game,  # action to perform when the button is clicked
            "text": "End Game" # text to display on the button
        }
        newGameButton = Button(self.colors, self.gameParams, newGameButtonParams) # Create new game button
        endGameButton = Button(self.colors, self.gameParams, endGameButtonParams)   # Create end game button
        newGameButton.draw() # Draw new game button
        endGameButton.draw() # Draw end game button

        for event in pygame.event.get(): # Check for events
            if event.type == pygame.QUIT: # If the user closes the window
                pygame.quit() # Quit the game
                sys.exit() # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse
                mouse_pos = pygame.mouse.get_pos() # Get the mouse position

                if newGameButton.click(mouse_pos): # If the new game button is clicked
                    self.new_game() # Start a new game
                    return # Exit the function
                elif endGameButton.click(mouse_pos): # If the end game button is clicked
                    self.end_game() # End the game
                    return # Exit the function

                '''
                if 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 450:
                    new_game()
                    return
                
                elif 500 <= mouse_pos[0] <= 650 and 400 <= mouse_pos[1] <= 450:
                    end_game()
                    return
                '''
        pygame.display.flip()  # Update the display