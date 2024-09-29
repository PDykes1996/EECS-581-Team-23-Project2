import pygame
import sys
from player import Player
from button import Button

class WinScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors
        self.gameParams = gameParams
    
    def new_game(self):
        self.gameParams["restart_game"] = True

    def end_game(self):
        self.gameParams["game_running"] = False

    def display(self, player):
        """
        Display the winner screen and options for a new game or to end the game.

        Args:
        player (int): The winning player number
        """
        self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen
        # Display winner text
        text = self.gameParams["font"].render(f"Player {player} Wins!", True, self.colors["BLACK"])
        self.gameParams["screen"].blit(text, (350, 200))

    # Draw new game and end game buttons
        newGameButtonParams = {
            "x": 300,
            "y": 400,
            "width": 150,
            "height": 50,
            "button_color": self.colors["LIGHT_GRAY"],
            "action": self.new_game,
            "text": "New Game"
        }
        endGameButtonParams = {
            "x": 500,
            "y": 400,
            "width": 150,
            "height": 50,
            "button_color": self.colors["LIGHT_GRAY"],
            "action": self.end_game,
            "text": "End Game"
        }
        newGameButton = Button(self.colors, self.gameParams, newGameButtonParams)
        endGameButton = Button(self.colors, self.gameParams, endGameButtonParams)
        newGameButton.draw()
        endGameButton.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if newGameButton.click(mouse_pos):
                        self.new_game()
                        return
                    elif endGameButton.click(mouse_pos):
                        self.end_game()
                        return

                '''
                if 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 450:
                    new_game()
                    return
                
                elif 500 <= mouse_pos[0] <= 650 and 400 <= mouse_pos[1] <= 450:
                    end_game()
                    return
                '''
        pygame.display.flip()  # Update the display