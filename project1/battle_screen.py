from player import Player
from button import Button
import sys
import pygame

class BattleScreen:
    
    #global finished, player1_sunk_ships, player2_sunk_ships, player1_hits, player2_hits

    
    # Determine which player's sunk ships to update
    #player_sunk_ships = player1_sunk_ships if player == 1 else player2_sunk_ships
    #opponent_sunk_ships = player2_sunk_ships if player == 1 else player1_sunk_ships
    #opponent_hits = player2_hits if player == 1 else player1_hits
    
    def __init__(self, gameParams, colors):
        self.gameParams = gameParams
        self.colors = colors

        self.playGridParams ={
            "grid_x" : 600,
            "grid_y" : 130,
            "cell_size" : 30,
            "font_offset_x" : 10,
            "font_offset_y" : 5,
            "line_thickness" : 2,
            "circle_radius" : 10,
        }
        """
        Display the battle screen where players make attacks.

        Args:
        player (int): The current player
        opponent_ships (list): List of opponent's ships
        hits_grid (list): Grid to track hits and misses
        player_ships (list): List of current player's ships

        Returns:
        int: 0 if no winner, or the winning player number
        """
    
    def draw_grid(self, grid_x, grid_y, label, hits_grid, ships, sunk_ships, opponent=False):
        # Draw grid label
        label_text = self.gameParams["font"].render(label, True, self.colors["BLACK"])
        self.gameParams["screen"].blit(label_text, (grid_x, grid_y - 60))

        # Draw the grid cells
        for i in range(10):
            for j in range(10):
                cell_x = grid_x + i * self.playGridParams["cell_size"]
                cell_y = grid_y + j * self.playGridParams["cell_size"]

                # Draw grid cell and border
                pygame.draw.rect(self.gameParams["screen"], self.colors["LIGHT_BLUE"], (cell_x, cell_y, self.playGridParams["cell_size"], self.playGridParams["cell_size"]))
                pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], (cell_x, cell_y, self.playGridParams["cell_size"], self.playGridParams["cell_size"]), 1)

                # Draw ships and hits for the player's grid
                if not opponent:
                    if any((j, i) in ship['coords'] for ship in ships):
                        pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (cell_x, cell_y, self.playGridParams["cell_size"], self.playGridParams["cell_size"]))
                    if (j, i) in [(y, x) for ship in sunk_ships for y, x in ship]:
                        pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], (cell_x, cell_y, self.playGridParams["cell_size"], self.playGridParams["cell_size"]))
                # Draw hit and miss markers
                if hits_grid[j][i] == 'M':
                    pygame.draw.circle(self.gameParams["screen"], self.colors["WHITE"], (cell_x + 15, cell_y + 15), 10, 2)
                elif hits_grid[j][i] == 'H':
                    pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (cell_x + 5, cell_y + 5), (cell_x + 25, cell_y + 25), 2)
                    pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (cell_x + 25, cell_y + 5), (cell_x + 5, cell_y + 25), 2)

    def handle_attack(self, event, player, opponent, hits_grid, opponent_sunk_ships):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (event.pos[0] - 50) // self.playGridParams["cell_size"], (event.pos[1] - 100) // self.playGridParams["cell_size"]
            if 0 <= x < 10 and 0 <= y < 10:
                if hits_grid[y][x] is None:
                    ship = self.get_ship(opponent, x, y)
                    if ship:
                        hits_grid[y][x] = 'H'  # Mark as hit
                        if self.check_ship_sunk(player, ship):
                            opponent_sunk_ships.append(ship['coords'])
                            return "Sink!"
                        else:
                            return "Hit!"
                    else:
                        hits_grid[y][x] = 'M'  # Mark as miss
                        return "Miss!"
                else:
                    return "Already Attacked!"
        return None

    def get_ship(self, opponent, x, y):
        """Find the ship at the given coordinates."""
        for ship in self.current_opponent.ships:
            if (y, x) in ship['coords']:
                return ship
        return None

    def check_ship_sunk(self, player, ship):
        """Check if all coordinates of a ship have been hit."""
        return all(player.hits[y][x] == 'H' for y, x in ship['coords'])


    def all_ships_sunk(self, player_ships):
        """Check if all ships of a player have been sunk."""
        return all(self.check_ship_sunk(ship) for ship in player_ships)

    def display(self, player):
        # Determine opponent
        opponent = self.gameParams["player2"] if player.player_id == 1 else self.gameParams["player1"]
        finished = False
        attack_made = False
        shot_result = None

        while not finished:
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear the screen

            # Display instruction for the current player
            text = self.gameParams["font"].render(f"Player {player.player_id}: Select a cell to attack", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (300, 20))

            # Draw the opponent's grid (for attacks) and player's own grid
            self.draw_grid(self.playGridParams["grid_x"], self.playGridParams["grid_y"], "Opponent's Grid", opponent.hits, opponent.ships, opponent.sunk_ships, opponent=True)
            self.draw_grid(600, 130, "Your Grid", player.hits, player.ships, player.sunk_ships)

            if shot_result:
                result_text = self.gameParams["font"].render(shot_result, True, self.colors["BLACK"])
                self.gameParams["screen"].blit(result_text, (400, 650))

            # Draw the finish turn button
            finish_turn_buttonParams = {
                "x": 800,
                "y": 600,
                "width": 150,
                "height": 50,
                "action": None,
                "text": "Finish Turn",
                "button_color": lambda: setattr(self, 'finished', True),
            }
            finish_turn_button = Button(self.colors, self.gameParams, finish_turn_buttonParams, enabled = attack_made )
            finish_turn_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not attack_made:
                    shot_result = self.handle_attack(event, player, opponent, player.hits, opponent.sunk_ships)
                    if shot_result:
                        attack_made = True

            pygame.display.flip()  # Update the display

            # Check for a winner
            if self.all_ships_sunk(opponent.ships):
                finished = True
                return player.player_id  # Return the winning player ID
            else:
                return 0  # Continue the game


    
