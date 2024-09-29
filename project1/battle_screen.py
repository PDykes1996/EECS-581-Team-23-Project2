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
    
    def __init__(self, colors, gameParams):
        self.gameParams = gameParams
        self.colors = colors
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
    
    def draw_grid(self, gridParams, opponent=False):
        # Extract game parameters
        screen = self.gameParams["screen"]
        font = self.gameParams["font"]
        # Extract grid parameters
        player = gridParams["player"]
        grid_x = gridParams["grid_x"]
        grid_y = gridParams["grid_y"]

        # Draw grid label
        label_text = font.render(gridParams["label"], True, self.colors["BLACK"])
        self.gameParams["screen"].blit(label_text, (grid_x, grid_y - 60))

        # Draw the grid cells
        for i in range(10):
            for j in range(10):
                cell_x = grid_x + i * gridParams["cell_size"]
                cell_y = grid_y + j * gridParams["cell_size"]

                # Draw grid cell and border
                pygame.draw.rect(screen, self.colors["LIGHT_BLUE"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                pygame.draw.rect(screen, self.colors["BLACK"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]), 1)

                # Draw ships and hits for the player's grid
                if not opponent:
                    if any((j, i) in ship['coords'] for ship in gridParams["player"].ships):
                        pygame.draw.rect(screen, self.colors["DARK_GRAY"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                    if (j, i) in [(y, x) for ship in player.sunk_ships for y, x in ship]:
                        pygame.draw.rect(screen, self.colors["RED"], (cell_x, cell_y, gridParams["cell_size"], gridParams["cell_size"]))
                # Draw hit and miss markers
                if player.hits[j][i] == 'M':
                    pygame.draw.circle(screen, self.colors["WHITE"], (cell_x + 15, cell_y + 15), 10, 2)
                elif player.hits[j][i] == 'H':
                    pygame.draw.line(screen, self.colors["RED"], (cell_x + 5, cell_y + 5), (cell_x + 25, cell_y + 25), 2)
                    pygame.draw.line(screen, self.colors["RED"], (cell_x + 25, cell_y + 5), (cell_x + 5, cell_y + 25), 2)

    def handle_attack(self, event, opponentGridParams):
        #Extract grid parameters
        #player = gridParams["player"] #Get player from the grid parameters
        #opponent = self.gameParams["player2"] if player.player_id == 1 else self.gameParams["player1"] #Get opponent from the game parameters
        opponent = opponentGridParams["player"] #Get player from the grid parameters

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (event.pos[0] - opponentGridParams["grid_x"]) // opponentGridParams["cell_size"], (event.pos[1] - opponentGridParams["grid_y"]) // opponentGridParams["cell_size"]
            if 0 <= x < 10 and 0 <= y < 10:
                if opponent.hits[y][x] is None:
                    ship = self.get_ship(opponent, x, y)
                    if ship:
                        opponent.hits[y][x] = 'H'  # Mark as hit
                        if self.check_ship_sunk(opponent, ship):
                            opponent.sunk_ships.append(ship['coords'])
                            return "Sink!"
                        else:
                            return "Hit!"
                    else:
                        opponent.hits[y][x] = 'M'  # Mark as miss
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


    def all_ships_sunk(self, player):
        """Check if all ships of a player have been sunk."""
        return all(self.check_ship_sunk(player, ship) for ship in player.ships)
    
    def end_turn(self):
        self.finished = True

    def display(self, player):
        # Extract game parameters
        screen = self.gameParams["screen"]
        font = self.gameParams["font"]
        # Determine opponent
        opponent = self.gameParams["player2"] if player.player_id == 1 else self.gameParams["player1"]
        self.finished = False
        attack_made = False
        shot_result = None

        while not self.finished:
            screen.fill(self.colors["WHITE"])  # Clear the screen

            # Display instruction for the current player
            text = font.render(f"Player {player.player_id}: Select a cell to attack", True, self.colors["BLACK"])
            screen.blit(text, (300, 20))


            opponentGridParams ={
            "player" : opponent,
            "label" : "Opponent's Grid",
            "grid_x" : 600,
            "grid_y" : 130,
            "cell_size" : 30,
            "font_offset_x" : 10,
            "font_offset_y" : 5,
            "line_thickness" : 2,
            "circle_radius" : 10,
            }
            playerGridParams ={
            "player" : player,
            "label" : "Your Grid",
            "grid_x" : 50,
            "grid_y" : 130,
            "cell_size" : 30,
            "font_offset_x" : 10,
            "font_offset_y" : 5,
            "line_thickness" : 2,
            "circle_radius" : 10,
            }

            # Draw the opponent's grid (for attacks) and player's own grid
            self.draw_grid(opponentGridParams, opponent=True)
            self.draw_grid(playerGridParams)

            if shot_result:
                result_text = font.render(shot_result, True, self.colors["BLACK"])
                screen.blit(result_text, (400, 650))

            # Draw the finish turn button
            finish_turn_buttonParams = {
                "x": 800,
                "y": 600,
                "width": 150,
                "height": 50,
                "action": self.end_turn,
                "text": "Finish Turn",
                "button_color": self.colors["LIGHT_GRAY"],
            }
            finish_turn_button = Button(self.colors, self.gameParams, finish_turn_buttonParams, enabled = attack_made )
            finish_turn_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


                if not attack_made:
                    shot_result = self.handle_attack(event, opponentGridParams)
                    if shot_result:
                        attack_made = True

            pygame.display.flip()  # Update the display

            # Check for a winner
            if self.all_ships_sunk(opponent):
                self.finished = True
                self.gameParams["winner"] = player
                return # Return the winning player ID
            if self.finished:
                return 0  # Continue the game


    
