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

# dict to hold game parameters
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

def main():
    """
    Main game loop that controls the flow of the game.
    """

    # loop that executes while game is running
    while gameParams["game_running"]:

        # listen for quit event (clicking the red X button) and quit the program when clicked
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # reinitialize all game parameter variables when user wants to start a new game
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
        
        # display the player 1's placement screen
        placementScreen.display(gameParams["player1"])
        #If player2 is a user, show their placement screen
        if not gameParams["player2"].isAI: placementScreen.display(gameParams["player2"])
        else: gameParams["player2"].place_AI_ships(gameParams["num_ships"])

        # execute the following loop until there is a winner
        while gameParams["winner"] == None:
            # Player 1's turn
            battleScreen.display(gameParams["player1"])
            # if there is a winner, break out of the loop
            if gameParams["winner"]:
                break

            # if player 2 is an AI, have the AI fire and return a winner (if there is one)
            if gameParams["player2"].isAI:
                winner = gameParams["player2"].fire(gameParams["player1"])
                if winner: gameParams["winner"] = winner

            # if player 2 is user, pass the screen to player 2, then display their board
            else:
                passScreen.display(gameParams["player2"])

                # Player 2's turn
                battleScreen.display(gameParams["player2"])
                # if there is a winner, break out of the loop
                if gameParams["winner"]:
                    break

                # otherwise pass the screen back to player 1
                passScreen.display(gameParams["player1"])


        # Display winner and handle game end or restart
        while gameParams["restart_game"] == False:
            winScreen.display(gameParams["winner"])
        
        # if game is not runninng, break out of the loop (which exits the program)
        if not gameParams["game_running"]:
            break

if __name__ == "__main__":
    main()