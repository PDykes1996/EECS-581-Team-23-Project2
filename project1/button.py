import pygame

class Button:
    def __init__(self, colors, gameParams, buttonParams, enabled = True):
        """
        Args:
        enabled (bool): Whether the button is clickable (Default is True)
        colors (dict): Dictionary containing color values
        {
            WHITE
            BLACK
            LIGHT_GRAY
            DARK_GRAY
            LIGHT_BLUE
            RED
            GRID_BLUE   
        }
        gameParams (dict):
        {
            "screen": Pygame screen object,
            "font": Pygame font object
            "game_running": Boolean to control game loop
            "finished": Boolean to end game
            "restart_game": Boolean to restart game
            "num_ships": Number of ships to place
            "player1": Player object for player 1
            "player2": Player object for player 2

        }
        buttonParams (dict):
        {
            "x": x-coordinate of the button
            "y": y-coordinate of the button
            "width": width of the button
            "height": height of the button
            "action": function to call when the button is clicked
            "text": text to display on the button
            "button_color": color of the button
        }
        """
        self.colors = colors #Color dictionary
        self.gameParams = gameParams #Game parameters dictionary
        self.enabled = enabled
        self.buttonParams = buttonParams

    def draw(self):
        """
        Draw an interactive button on the screen.

        Args:
        text (str): Text to display on the button
        x, y (int): Top-left coordinates of the button
        w, h (int): Width and height of the button
        color (tuple): RGB color of the button
        action (function): Function to call when the button is clicked
        enabled (bool): Whether the button is clickable
        """

        #Assign button parameters with default cases in case they are not provided
        x = self.buttonParams.get("x", 0)
        y = self.buttonParams.get("y", 0)
        width = self.buttonParams.get("width", 100)
        height = self.buttonParams.get("height", 50)
        button_color = self.buttonParams.get("button_color", self.colors["LIGHT_GRAY"])
        action = self.buttonParams.get("action", None) #Get the action function if it exists
        text = self.buttonParams["text"]

        self.rect = pygame.Rect(x, y, width, height)  # Initialize rect

        mouse = pygame.mouse.get_pos()  # Get current mouse position
        click = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

        # Draw the button rectangle
        if self.enabled:
            pygame.draw.rect(self.gameParams["screen"], button_color, (x, y, width, height))
        else:
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (x, y, width, height))  # Use dark gray for disabled buttons

        # Check if the mouse is over the button
        if self.enabled and self.rect.collidepoint(mouse):
            # Change button color on hover
            pygame.draw.rect(self.gameParams["screen"], self.colors["LIGHT_BLUE"], self.rect)
            if click[0] == 1 and not self.button_clicked:
                self.button_clicked = True
                if action:
                    action()
            elif click[0] == 0:
                self.button_clicked = False
        else:
            pygame.draw.rect(self.gameParams["screen"], button_color, self.rect)

        # Render button text
        text_color = self.colors["BLACK"] if self.enabled else self.colors["LIGHT_GRAY"]
        text_surf = self.gameParams["font"].render(text, True, self.colors["BLACK"])
        text_pos = (x + width // 2 - text_surf.get_width() // 2, y + height // 2 - text_surf.get_height() // 2)
        self.gameParams["screen"].blit(text_surf, text_pos)

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)