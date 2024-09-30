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
        self.enabled = enabled #Whether the button is clickable
        self.buttonParams = buttonParams #Button parameters dictionary
        self.button_clicked = False #Whether the button has been clicked
        self.rect = None #Rectangle object for the button

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
        x = self.buttonParams.get("x", 0) # Get x-coordinate of the button
        y = self.buttonParams.get("y", 0) # Get y-coordinate of the button
        width = self.buttonParams.get("width", 100) # Get width of the button
        height = self.buttonParams.get("height", 50) # Get height of the button
        button_color = self.buttonParams.get("button_color", self.colors["LIGHT_GRAY"]) # Get button color
        action = self.buttonParams.get("action", None) #Get the action function if it exists
        text = self.buttonParams["text"] # Get text to display on the button

        self.rect = pygame.Rect(x, y, width, height)  # Initialize rect

        mouse = pygame.mouse.get_pos()  # Get current mouse position
        click = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

        # Draw the button rectangle
        if self.enabled:
            pygame.draw.rect(self.gameParams["screen"], button_color, (x, y, width, height)) # Use button color
        else:
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (x, y, width, height))  # Use dark gray for disabled buttons

        # Check if the mouse is over the button
        if self.enabled and self.rect.collidepoint(mouse):
            # Change button color on hover
            pygame.draw.rect(self.gameParams["screen"], self.colors["LIGHT_BLUE"], self.rect)  # Light blue on hover
            if click[0] == 1 and not self.button_clicked: # Check if the left mouse button is clicked
                self.button_clicked = True # Set button_clicked to True
                if action: # Call the action function if it exists
                    action() # Call the action function
            elif click[0] == 0: # Reset button_clicked when the mouse button is released
                self.button_clicked = False # Set button_clicked to False
        else:
            pygame.draw.rect(self.gameParams["screen"], button_color, self.rect)  # Draw button with original color

        # Render button text
        text_color = self.colors["BLACK"] if self.enabled else self.colors["LIGHT_GRAY"] # Set text color based on button state
        text_surf = self.gameParams["font"].render(text, True, self.colors["BLACK"]) # Create text surface
        text_pos = (x + width // 2 - text_surf.get_width() // 2, y + height // 2 - text_surf.get_height() // 2) # Center text
        self.gameParams["screen"].blit(text_surf, text_pos) # Display text

    def click(self, mouse_pos): # Check if the button is clicked
        return self.rect.collidepoint(mouse_pos) # Return True if the mouse is over the button