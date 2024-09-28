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
    
    def __init__(self, players, gameParams):
        #self.screen = screen
        self.player1 = players[0]
        self.player2 = players[1]
        self.current_player = self.player1  # newly added
        self.current_opponent = self.player2 # newly added
        print(self.player1, self.player2, self.current_player, self.current_opponent)
        self.finished = False
        self.shot_result = None  # Stores the result of the latest attack
        self.attack_made = False  # Flag to track if an attack has been made this turn
        self.gameParams = gameParams        # newly added
        self.attack_made = False

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
    

    def get_ship(self, x, y):
        """Find the ship at the given coordinates."""
        for ship in self.current_opponent.ships:
            if (y, x) in ship['coords']:
                return ship
        return None

    def check_ship_sunk(self, ship):
        """Check if all coordinates of a ship have been hit."""
        return all(self.current_player.hits[y][x] == 'H' for y, x in ship['coords'])


    def display(self, player):
        # until battlescreen is finished...
        while not self.finished:
            self.gameParams['screen'].fill(WHITE)  # initialize the screen to be white
            text = self.gameParams['font'].render(f"Player {player}: Select a cell to attack", True, BLACK) # initialize text
            self.gameParams['screen'].blit(text, (300, 20))     # blit the text to the screen

            # Draw opponent's grid (for attacks)
            for i in range(10):
                for j in range(10):
                    pygame.draw.rect(self.gameParams["screen"], GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                    pygame.draw.rect(self.gameParams['screen'], BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)
                    self.gameParams['screen'].blit(self.gameParams['font'].render(chr(65 + i), True, BLACK), (65 + i * 50, 70))
                    self.gameParams['screen'].blit(self.gameParams['font'].render(str(j + 1), True, BLACK), (20, 115 + j * 50))

                    # Draw hit and miss markers
                    if self.current_opponent.hits[j][i] == 'M':
                        pygame.draw.circle(self.gameParams['screen'], WHITE, (75 + i * 50, 125 + j * 50), 20, 2)
                    elif self.current_opponent.hits[j][i] == 'H':
                        ship = self.get_ship(i, j)
                        if ship and ship['coords'] in self.current_opponent.sunk_ships:
                            pygame.draw.rect(self.gameParams['screen'], RED, (50 + i * 50, 100 + j * 50, 50, 50))
                        else:
                            pygame.draw.line(self.gameParams['screen'], RED, (60 + i * 50, 110 + j * 50), (90 + i * 50, 140 + j * 50), 3)
                            pygame.draw.line(self.gameParams['screen'], RED, (90 + i * 50, 110 + j * 50), (60 + i * 50, 140 + j * 50), 3)

        # Draw player's own grid
            your_grid_text = self.gameParams['font'].render("Your Grid", True, BLACK)
            self.gameParams['screen'].blit(your_grid_text, (600, 70))
            for i in range(10):
                for j in range(10):
                    pygame.draw.rect(self.gameParams['screen'], LIGHT_BLUE, (600 + i * 30, 130 + j * 30, 30, 30))
                    pygame.draw.rect(self.gameParams['screen'], BLACK, (600 + i * 30, 130 + j * 30, 30, 30), 1)
                    self.gameParams['screen'].blit(self.gameParams['font'].render(chr(65 + i), True, BLACK), (610 + i * 30, 100))
                    self.gameParams['screen'].blit(self.gameParams['font'].render(str(j + 1), True, BLACK), (570, 135 + j * 30))

                    # Draw player's ships and hit markers
                    if any((j, i) in ship['coords'] for ship in self.current_player.ships):
                        pygame.draw.rect(self.gameParams['screen'], DARK_GRAY, (600 + i * 30, 130 + j * 30, 30, 30))
                    if (j, i) in [(y, x) for ship in self.current_player.sunk_ships for y, x in ship]:
                        pygame.draw.rect(self.gameParams['screen'], RED, (600 + i * 30, 130 + j * 30, 30, 30))
                    elif self.current_opponent.hits[j][i] == 'H':
                        pygame.draw.line(self.gameParams['screen'], RED, (605 + i * 30, 135 + j * 30), (625 + i * 30, 155 + j * 30), 2)
                        pygame.draw.line(self.gameParams['screen'], RED, (625 + i * 30, 135 + j * 30), (605 + i * 30, 155 + j * 30), 2)
                    elif self.current_opponent.hits[j][i] == 'M':
                        pygame.draw.circle(self.gameParams['screen'], WHITE, (615 + i * 30, 145 + j * 30), 10, 2)

            if self.shot_result:
                result_text = self.gameParams['font'].render(self.shot_result, True, BLACK)
                self.gameParams['screen'].blit(result_text, (400, 650))

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


    # Check for a winner
    if all_ships_sunk(opponent_ships):
        finished = True
        winner = player
        return winner
    else:
        return 0
"""