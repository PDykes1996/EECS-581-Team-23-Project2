from player import Player
from button import Button
import sys
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 100, 255)
GRID_BLUE = (10, 150, 210)

colors = {
    'WHITE' : (255, 255, 255),
    'BLACK' : (0, 0, 0),
    'RED' : (255, 0, 0),
    'LIGHT_GRAY' : (200, 200, 200),
    'DARK_GRAY' : (150, 150, 150),
    'LIGHT_BLUE' : (100, 100, 255),
    'GRID_BLUE' : (10, 150, 210)
}


class BattleScreen:
    
    #global finished, player1_sunk_ships, player2_sunk_ships, player1_hits, player2_hits

    
    # Determine which player's sunk ships to update
    #player_sunk_ships = player1_sunk_ships if player == 1 else player2_sunk_ships
    #opponent_sunk_ships = player2_sunk_ships if player == 1 else player1_sunk_ships
    #opponent_hits = player2_hits if player == 1 else player1_hits
    
    def _init_(self, gameParams, colors):
        self.gameParams = gameParams
        self.colors = colors

        playGridParams ={
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
        if player.player_id == 1:
            opponent = self.gameParams["player2"]
        else:
            opponent = self.gameParams["player1"]

        while not finished:
            self.screen.fill(self.gameParams["WHITE"])  # Clear screen
            # Display player instruction
            text = self.gameParams["font"].render(f"Player {player}: Select a cell to attack", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (300, 20))

            # Draw opponent's grid (for attacks)
            for i in range(10):
                for j in range(10):
                    pygame.draw.rect(self.gameParams["screen"], self.colors["GRID_BLUE"], (50 + i * 50, 100 + j * 50, 50, 50))
                    pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], (50 + i * 50, 100 + j * 50, 50, 50), 1)
                    self.gameParams["screen"].blit(self.gameParams["font"].render(chr(65 + i), True, self.colors["BLACK"]), (65 + i * 50, 70))
                    self.gameParams["screen"].blit(self.gameParams["font"].render(str(j + 1), True, self.colors["BLACK"]), (20, 115 + j * 50))

                    # Draw hit and miss markers
                    if player.hits[j][i] == 'M':
                        pygame.draw.circle(self.gameParams["screen"], self.colors["WHITE"], (75 + i * 50, 125 + j * 50), 20, 2)
                    elif player.hits[j][i] == 'H':
                        ship = self.get_ship(i, j)
                        if ship and ship['coords'] in opponent.sunk_ships:
                            pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], (50 + i * 50, 100 + j * 50, 50, 50))
                        else:
                            pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (60 + i * 50, 110 + j * 50), (90 + i * 50, 140 + j * 50), 3)
                            pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (90 + i * 50, 110 + j * 50), (60 + i * 50, 140 + j * 50), 3)

        # Draw player's own grid
            your_grid_text = self.gameParams["font"].render("Your Grid", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(your_grid_text, (600, 70))
            for i in range(10):
                for j in range(10):
                    cell_top_left_x = 

                    pygame.draw.rect(self.gameParams["screen"], self.colors["LIGHT_BLUE"], (600 + i * 30, 130 + j * 30, 30, 30))
                    pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], (600 + i * 30, 130 + j * 30, 30, 30), 1)
                    self.gameParams["screen"].blit(self.gameParams["font"].render(chr(65 + i), True, self.colors["BLACK"]), (610 + i * 30, 100))
                    self.gameparams["screen"].blit(self.gameParams["font"].render(str(j + 1), True, self.colors["BLACK"]), (570, 135 + j * 30))

                    # Draw player's ships and hit markers
                    if any((j, i) in ship['coords'] for ship in player.ships):
                        pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (600 + i * 30, 130 + j * 30, 30, 30))
                    if (j, i) in [(y, x) for ship in player.sunk_ships for y, x in ship]:
                        pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], (600 + i * 30, 130 + j * 30, 30, 30))
                    elif opponent.hits[j][i] == 'H':
                        pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (605 + i * 30, 135 + j * 30), (625 + i * 30, 155 + j * 30), 2)
                        pygame.draw.line(self.gameParams["screen"], self.colors["RED"], (625 + i * 30, 135 + j * 30), (605 + i * 30, 155 + j * 30), 2)
                    elif opponent.hits[j][i] == 'M':
                        pygame.draw.circle(self.gameParams["screen"], self.colors["WHITE"], (615 + i * 30, 145 + j * 30), 10, 2)

            if shot_result:
                result_text = font.render(shot_result, True, self.colors["BLACK"])
                screen.blit(result_text, (400, 650))

            # Draw finish turn button
            # need this function from the button class
            finish_turn_button = Button(colors, self.gameParams, 800, 600, 150, 50, LIGHT_GRAY, "Finish Turn")
            finish_turn_button.draw(800, 600, 150, 50,
                    lambda: locals().update(finished=True),
                    enabled=self.attack_made)
            #draw_button("Finish Turn", 800, 600, 150, 50, LIGHT_GRAY, lambda: locals().update(finished=True),
                    #enabled=attack_made)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.attack_made:
                    x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                    if 0 <= x < 10 and 0 <= y < 10:
                        if self.current_player.hits[y][x] is None:
                            ship = self.get_ship(x, y)
                            if ship:
                                self.current_player.hits[y][x] = 'H'  # Mark as hit
                                if self.check_ship_sunk(ship):
                                    self.current_player.sunk_ships.append(ship['coords'])
                                    self.shot_result = "Sink!"
                                else:
                                    self.shot_result = "Hit!"
                            else:
                                self.current_player.hits[y][x] = 'M'  # Mark as miss
                                self.shot_result = "Miss!"
                            self.attack_made = True
                        else:
                            self.shot_result = "Already Attacked!"

            pygame.display.flip()  # Update the display

            # Check for a winner
        if all_ships_sunk(opponent_ships):
            finished = True
            winner = player
            return winner
        else:
            return 0

    # Update sunk ships for the correct player
        if player == 1:
            self.player2 = self.current_opponent #player2_sunk_ships = opponent_sunk_ships
            self.player1 = self.current_player
        else:
            self.player1 = self.current_opponent #player1_sunk_ships = opponent_sunk_ships
            self.player2 = self.current_player

# this might go in the win screen file??
"""
    def all_ships_sunk(self, player_ships):
        #Check if all ships of a player have been sunk.
        return all(self.check_ship_sunk(ship) for ship in player_ships)
"""


    
