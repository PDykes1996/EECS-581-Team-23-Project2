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

        x = self.buttonParams["x"]
        y = self.buttonParams["y"]
        width = self.buttonParams["width"]
        height = self.buttonParams["height"]
        action = self.buttonParams["action"]
        text = self.buttonParams["text"]
        button_color = self.buttonParams["button_color"]

        self.rect = pygame.Rect(x, y, width, height)  # Initialize rect

        mouse = pygame.mouse.get_pos()  # Get current mouse position
        click = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

        # Draw the button rectangle
        if self.enabled:
            pygame.draw.rect(self.gameParams["screen"], button_color, (x, y, width, height))
        else:
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (x, y, width, height))  # Use dark gray for disabled buttons

        #Render the button text
        text_surf = self.gameParams["font"].render(text, True, self.colors["BLACK"])
        # Calculate position to center the text on the button
        text_pos = (x + width // 2 - text_surf.get_width() // 2, y + height // 2 - text_surf.get_height() // 2)
        self.gameParams["screen"].blit(text_surf, text_pos)

        # Check if the mouse is over the button and it's clicked
        if self.enabled and x < mouse[0] < x + width and y < mouse[1] < y + height:
            if click[0] == 1 and action is not None:
                action()  # Execute the given action when clicked

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)