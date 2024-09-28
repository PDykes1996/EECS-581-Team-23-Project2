import pygame
import sys

from button import Button
class StartScreen:
    def __init__(self, gameParams, colorDict):
        self.colors = colorDict
        self.gameParams = gameParams
    
    def display(self, screen, font):
        """
        Display the start screen where players select the number of ships.
        """
        while self.gameParams["num_ships"] == 0:  # Loop until a number of ships is selected
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear the screen using white background
            text = font.render("Select number of ships to play with:", True, self.colors["BLACK"])
            screen.blit(text, (250, 200))

            # Create buttons for ship selection (1 to 5 ships)
            for i in range(1, 6):
                # Lambda function to set num_ships when a button is clicked
                ship_num_buttonParams ={
                    "x" : int(150+100*i),
                    "y" : 250,
                    "width" : 80,
                    "height" : 50,
                    "button_color" : self.colors["LIGHT_GRAY"],
                    "action" : lambda i=i: setattr(self.gameParams, 'num_ships', i),
                    "text" : str(i),
                }
                
                
                numSelector = Button(self.colors, self.gameParams, ship_num_buttonParams)
                numSelector.draw(ship_num_buttonParams)

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the display