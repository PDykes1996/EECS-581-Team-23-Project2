""""
script.py

Project 1

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


Project 2

Description:
This program implements a one or two-player Battleship game using Pygame. 
Players can place ships on a grid and take turns attacking each other's ships.
Option to play against AI with three levels of difficulty

Inputs:
- Mouse clicks for ship placement and attacks
- Keyboard input for rotating ships during placement
- Difficulty Level
- Number of ships
- PvP or PvAI

Output:
- Graphical display of the game board, ship placements, and attack results

Other sources:
- Chat GPT for how pygame displays and how to use lambda functions
- Various Stack Overflow pages

Authors: John Mosley, Paul Dykes, Willem Battey, Aryamann Zutshi, Spencer Addis
Creation date: 9/26/2024
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
#Initialize other screens with new game parameters
startScreen = StartScreen(gameParams, colorDict)        #Start screen to select number of ships, game mode, and AI difficulty
placementScreen = PlacementScreen(colorDict, gameParams)#Placement screen to place ships
passScreen = PassScreen(colorDict, gameParams)          #Pass screen to switch turns
battleScreen = BattleScreen(colorDict, gameParams)      #Battle screen to display the game board
winScreen = WinScreen(colorDict, gameParams)            #Win screen to display the winner and options to restart or end the game


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
            gameParams["winner"] = None # Reset winner
            gameParams["num_ships"] = 0 # Reset number of ships
            #Reset ship lists and hits grids to empty lists
            gameParams["player1"].ships = []
            gameParams["player2"].ships = []  
            gameParams["player1"].sunk_ships = []
            gameParams["player2"].sunk_ships = []
            gameParams["player1"].hits = [[None for _ in range(10)] for _ in range(10)]  # Reset the hits grid
            gameParams["player2"].hits = [[None for _ in range(10)] for _ in range(10)]  # Same for player2

            gameParams["player1"].special_used = False # Enable special ability P1
            gameParams["player2"].special_used = False # Enable special ability P2
            gameParams["restart_game"] = False
            continue

        startScreen.display() # Start screen to select number of ships

        placementScreen.display(gameParams["player1"])                                      # display player 1's placement screen...
        if not gameParams["player2"].isAI: placementScreen.display(gameParams["player2"])   #...if player2 is a user, show their placement screen...
        else: gameParams["player2"].place_AI_ships(gameParams["num_ships"])                 #...otherwise, place AI ships

        # Game Loop
        while gameParams["winner"] == None:             # While there is no winner...
            # Player 1's turn
            battleScreen.display(gameParams["player1"]) #...display player 1's board
            if gameParams["winner"]:                    #...If player 1 wins...
                break                                   #...end the loop

            # Player 2 (AI) Turn Loop
            if gameParams["player2"].isAI:                                  #If player 2 is an AI...
                winner = gameParams["player2"].fire(gameParams["player1"])  #...have the AI fire at player 1...
                if winner: gameParams["winner"] = winner                    #... and if player 2 wins, set them as the winner

            # Player 2 (Human) Turn Loop
            else:
                passScreen.display(gameParams["player2"])   #Display the pass screen for player 2...

                battleScreen.display(gameParams["player2"]) #...display player 2's board
                if gameParams["winner"]:                    #...If player 2 wins...
                    break                                   #...end the loop
                passScreen.display(gameParams["player1"])   #...Otherwise, pass the turn back to player 1


        while gameParams["restart_game"] == False and gameParams["game_running"]: #While the game is running and hasn't been restarted...
            winScreen.display(gameParams["winner"])                               #...display the win screen until player chooses to restart or end the game
        
        if not gameParams["game_running"]: #If the game has ended and not been restarted...
            break                          #...end the game loop

if __name__ == "__main__":
    main()