import pygame
import sys
from player import Player
from button import Button

class PlacementScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors
        self.gameParams = gameParams

    def display(self, player):
        """
        Display the ship placement screen for a player.

        Args:
        player (int): The player number (1 or 2)
        """
        # Initialize empty grid and ships for placement
        grid = [[None] * 10 for _ in range(10)]
        ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(self.gameParams["num_ships"])]
        selected = None  # Currently selected ship
        vertical = False  # Ship orientation (horizontal by default)
        finished = False  # Flag to track when placement is complete

        while not finished:
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen

            # Display player instruction
            self._draw_text(f"Player {player} Ship Placement", (350, 20))

            # Draw the placement grid
            self._draw_grid(grid)

            # Draw the ships in the side panel
            self._draw_ships(ships, selected)

            # Check if all ships are placed
            all_ships_placed = all(ship.left < 600 for ship in ships)

            # Create Rotate and Finish buttons
            rotateButton = Button(
                self.colors, self.gameParams,
                {"x": 600, "y": 600, "width": 150, "height": 50, "button_color": self.colors["LIGHT_GRAY"],
                 "action": lambda: self._toggle_orientation(vertical), "text": "Rotate (V)" if vertical else "Rotate (H)"}
            )
            finishButton = Button(
                self.colors, self.gameParams,
                {"x": 800, "y": 600, "width": 150, "height": 50, "button_color": self.colors["LIGHT_GRAY"],
                 "action": lambda: self._finish_placement(finished, all_ships_placed), "text": "Finish"}
            )

            rotateButton.draw()
            finishButton.draw()

            # Show placement indicator
            mouse_pos = pygame.mouse.get_pos()
            if selected is not None:
                self._draw_placement_indicator(ships[selected], mouse_pos, vertical)

            # Handle user inputs
            self._handle_events(ships, selected, vertical, finished, grid)

            # Update the display
            pygame.display.flip()

        # Store the placed ships for each player
        self._store_ships(player, grid)

    def _draw_text(self, text, pos):
        """Helper function to render and display text."""
        rendered_text = self.gameParams["font"].render(text, True, self.colors["BLACK"])
        self.gameParams["screen"].blit(rendered_text, pos)

    def _draw_grid(self, grid):
        """Helper function to draw the placement grid."""
        for i in range(10):
            for j in range(10):
                rect = pygame.Rect(50 + i * 50, 100 + j * 50, 50, 50)
                pygame.draw.rect(self.gameParams["screen"], self.colors["GRID_BLUE"], rect)
                pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], rect, 1)

                if grid[j][i] is not None:
                    pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], rect)

                # Draw grid labels (A-J, 1-10)
                self._draw_text(chr(65 + i), (65 + i * 50, 70))
                self._draw_text(str(j + 1), (20, 115 + j * 50))

    def _draw_ships(self, ships, selected):
        """Helper function to draw ships in the side panel."""
        for i, ship in enumerate(ships):
            pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], ship)
            if i == selected:
                pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], ship, 2)  # Highlight selected ship

    def _draw_placement_indicator(self, ship, mouse_pos, vertical):
        """Draw a placement indicator for the selected ship."""
        size = max(ship.width, ship.height) // 50
        if vertical:
            indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size * 50)
        else:
            indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size * 50, 50)
        pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], indicator, 2)

    def _toggle_orientation(self, vertical):
        """Toggle ship orientation."""
        return not vertical

    def _finish_placement(self, finished, all_ships_placed):
        """Finish ship placement if all ships are placed."""
        if all_ships_placed:
            finished = True

    def _handle_events(self, ships, selected, vertical, finished, grid):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    vertical = False
                elif event.key == pygame.K_v:
                    vertical = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event, ships, selected, vertical, grid)

    def _handle_mouse_click(self, event, ships, selected, vertical, grid):
        """Handle mouse clicks for ship placement and selection."""
        x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
        if 0 <= x < 10 and 0 <= y < 10:
            if selected is not None:
                size = max(ships[selected].width, ships[selected].height) // 50
                if self.is_valid_placement(x, y, size, vertical, selected + 1, grid):
                    self.clear_ship(selected + 1, grid)  # Clear old position of the ship

                    # Place the ship on the grid based on orientation
                    for i in range(size):
                        if vertical:
                            grid[y + i][x] = selected + 1  # Place ship vertically
                        else:
                            grid[y][x + i] = selected + 1  # Place ship horizontally

                    # Update ship position in the 'ships' list with correct orientation
                    ships[selected] = pygame.Rect(
                        50 + x * 50, 100 + y * 50,
                        50 if vertical else size * 50,
                        size * 50 if vertical else 50
                    )
                    selected = None  # Deselect the ship after placing it

            else:
                # Select a ship from the side panel
                for i, ship in enumerate(ships):
                    if ship.collidepoint(event.pos):
                        selected = i
                        self.clear_ship(i + 1, grid)  # Clear the ship's current position in the grid
                        break

    def clear_ship(self, ship_num, grid):
        """Remove a ship from the grid."""
        for y in range(10):
            for x in range(10):
                if grid[y][x] == ship_num:
                    grid[y][x] = None

    def is_valid_placement(self, x, y, size, is_vertical, ship_num, grid):
        """Check if a ship placement is valid."""
        # Check if ship is within grid bounds
        if is_vertical and y + size > 10:
            return False
        if not is_vertical and x + size > 10:
            return False

        # Check for overlap with other ships
        for i in range(size):
            check_x = x + (0 if is_vertical else i)
            check_y = y + (i if is_vertical else 0)

            if grid[check_y][check_x] is not None and grid[check_y][check_x] != ship_num:
                return False

        return True

    def _store_ships(self, player, grid):
        """Store the placed ships in the game parameters."""
        if player == 1:
            self.gameParams["player1"].ships = [
                {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in range(self.gameParams["num_ships"])
            ]
        else:
            self.gameParams["player2"].ships = [
                {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in range(self.gameParams["num_ships"])
            ]       