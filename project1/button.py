import pygame

class Button:
    def __init__(self, colors, gameParams, buttonParams, enabled = True):
        self.colors = colors #Color dictionary
        self.gameParams = gameParams #Game parameters dictionary
        self.enabled = enabled

        self.x = buttonParams["x"]
        self.y = buttonParams["y"]
        self.width = buttonParams["width"]
        self.height = buttonParams["height"]
        self.action = buttonParams["action"]
        self.text = buttonParams["text"]

    def draw(self, buttonParams):
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
        mouse = pygame.mouse.get_pos()  # Get current mouse position
        click = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

        # Draw the button rectangle
        if self.enabled:
            pygame.draw.rect(self.gameParams["screen"], buttonParams["button_color"], (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (self.x, self.y, self.width, self.height))  # Use dark gray for disabled buttons

        #Render the button text
        text_surf = self.gameParams["font"].render(self.text, True, self.colors["BLACK"])
        # Calculate position to center the text on the button
        text_pos = (self.x + self.width // 2 - text_surf.get_width() // 2, self.y + self.height // 2 - text_surf.get_height() // 2)
        self.gameParams["screen"].blit(text_surf, text_pos)

        # Check if the mouse is over the button and it's clicked
        if self.enabled and self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            if click[0] == 1 and self.action is not None:
                self.action()  # Execute the given action when clicked

    def click(self, mouse_pos):
        return self.rect.collidepoint