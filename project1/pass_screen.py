from button import Button
import pygame
import sys

class PassScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors # Dictionary of colors
        self.gameParams = gameParams

    def display(self, player):
        """
        Display a screen to pass control to the next player.

        Args:
        player (Player): The player to pass control to
        """
        finished = False
        while not finished:
            passButtonParams ={
                "x": 400,
                "y": 600,
                "width": 150,
                "height": 50,
                "action": lambda: globals().update(finished=True),
                "text": "Finish",
                "button_color": self.colors["LIGHT_GRAY"] ,
            }
            passButton = Button(self.colors, self.gameParams, passButtonParams)

            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen
            # Display pass instruction
            text = self.gameParams["font"].render(f"Pass to player {player.player_id}", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (350, 20))
            # Draw finish button
            passButton.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 400 <= event.pos[0] <= 550 and 600 <= event.pos[1] <= 650:
                        finished = True  # Finish button clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()  # Update the display
        