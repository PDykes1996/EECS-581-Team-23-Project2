from button import Button
import pygame
import sys

class PassScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors # Dictionary of colors
        self.gameParams = gameParams # pass game parameters in

    def display(self, player):
        """
        Display a screen to pass control to the next player.

        Args:
        player (Player): The player to pass control to
        """
        finished = False # state to detect if pass is finished
        while not finished:
            passButtonParams ={ # button parameters for Finish Passing button
                "x": 400, # dimensions
                "y": 600,
                "width": 150,
                "height": 50,
                "action": lambda: globals().update(finished=True), # action
                "text": "Finish", # Finish label
                "button_color": self.colors["LIGHT_GRAY"] # color
            }
            passButton = Button(self.colors, self.gameParams, passButtonParams) # button created

            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen
            # Display pass instruction
            text = self.gameParams["font"].render(f"Pass to player {player.player_id}", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (350, 20))
            passButton.draw() # Draw finish button

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 400 <= event.pos[0] <= 550 and 600 <= event.pos[1] <= 650:
                        finished = True  # Finish button clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # exit this program

            pygame.display.flip()  # Update the display
        