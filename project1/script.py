""""
script.py

Description:
This program implements a two-player Battleship game using Pygame. Players can place ships on a grid and take turns attacking each other's ships.

Inputs:
- Mouse clicks for ship placement and attacks
- Keyboard input for rotating ships during placement

Output:
- Graphical display of the game board, ship placements, and attack results

Other sources:
- Pygame documentation for GUI implementation
- Claude 3.5 Sonnet for debugging and optimization suggestions
- Various Stack Overflow and GeeksforGeeks pages

Authors: Ethan Dirkes, Chase Entwistle, Christopher Gronewold, Tommy Lam, Zonaid Prithu
Creation date: 9/6/2024
"""

import pygame
import sys
from player import Player
from start_screen import StartScreen
from battle_screen import BattleScreen
from pass_screen import PassScreen
from placement_screen import PlacementScreen
from win_screen import WinScreen

# Initialize Pygame and set up the display
pygame.init()


gameParams = {
    "winner" : None,
    "game_running": True,
    "restart_game": False,
    "num_ships": 0,
    "player1" : Player(1),
    "player2" : Player(2),
    "screen" : pygame.display.set_mode((1000, 750)), #1000x750 pixel window
    "font" : pygame.font.Font(None,36), #Default font for text
}

# Define color constants for easy reference throughout the game
colorDict = {
    "WHITE" : (255, 255, 255),
    "BLACK" : (0, 0, 0),
    "LIGHT_GRAY" : (200, 200, 200),
    "DARK_GRAY" : (150, 150, 150),
    "LIGHT_BLUE" : (100, 100, 255),
    "RED" : (255, 0, 0),
    "GRID_BLUE" : (10, 150, 210),
}

#Initializing Player information

# Lists to store sunk ships for each player

def main():
    """
    Main game loop that controls the flow of the game.
    """
    clock = pygame.time.Clock()

    while gameParams["game_running"]:

        for event in pygame.event.get():
           if event.type == pygame.QUIT:
            gameParams["game_running"] = False
            pygame.quit()
            sys.exit()

        if gameParams["restart_game"]:
            # Reset all game variables for a new game
            gameParams["num_ships"] = 0
            gameParams["player1"].ships = None
            gameParams["player2"].ships = None
            gameParams["player1"].sunk_ships = []
            gameParams["player2"].sunk_ships = []
            gameParams["player1"].hits = None
            gameParams["player2"].hits = None
            gameParams["restart_game"] = False
            continue
        
        # Start screen to select number of ships
        startScreen = StartScreen(gameParams, colorDict)
        startScreen.display()

        #Initialize other screens with new game parameters
        placementScreen = PlacementScreen(colorDict, gameParams)
        passScreen = PassScreen(colorDict, gameParams)
        battleScreen = BattleScreen(colorDict, gameParams)
        winScreen = WinScreen(colorDict, gameParams)

        placementScreen.display(gameParams["player1"])
        placementScreen.display(gameParams["player2"])




        while gameParams ["winner"] == None:
            # Player 1's turn
            winner = battleScreen.display(gameParams["player1"])
            if winner:
                break
            passScreen.display(gameParams["player2"])

            # Player 2's turn
            winner = battleScreen.display(gameParams["player2"])
            if winner:
                break
            passScreen.display(gameParams["player1"])

        # Display winner and handle game end or restart
        winScreen.display(winner)

        if not gameParams["game_running"]:
            break

if __name__ == "__main__":
    main()