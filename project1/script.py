import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 750))
font = pygame.font.Font(None, 36)

# Define color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)  # for grayed out buttons and ships
LIGHT_BLUE = (100, 100, 255)
RED = (255, 0, 0)  # for outlining ships
GRID_BLUE = (10, 150, 210)  # for grid background

# Global variables to store game state
num_ships = 0
player1_ships = None
player2_ships = None

# Grids to track attacks for each player
player1_attack_grid = [[None for _ in range(10)] for _ in range(10)]
player2_attack_grid = [[None for _ in range(10)] for _ in range(10)]

def draw_button(text, x, y, w, h, color, action=None, enabled=True):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw the button in dark gray if it's disabled
    if enabled:
        pygame.draw.rect(screen, color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))

    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + w // 2 - text_surf.get_width() // 2, y + h // 2 - text_surf.get_height() // 2))

    # Check if the button is clicked and execute the associated action
    if enabled and x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1 and action is not None:
            action()

def start_screen():
    global num_ships
    while num_ships == 0:
        screen.fill(WHITE)
        text = font.render("Select number of ships to play with:", True, BLACK)
        screen.blit(text, (250, 200))

        # Draw buttons for selecting the number of ships (1 to 5)
        for i in range(1, 6):
            draw_button(str(i), 150 + 100 * i, 250, 80, 50, LIGHT_GRAY,
                        lambda i=i: setattr(sys.modules[__name__], 'num_ships', i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

finished = False

def placement_screen(player):
    global player1_ships, player2_ships, finished
    grid = [[None] * 10 for _ in range(10)]  # Initialize the grid with None values
    ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(num_ships)]
    selected = None
    vertical = False
    finished = False

    def clear_ship(ship_num):
        # Remove a ship from the grid
        for y in range(10):
            for x in range(10):
                if grid[y][x] == ship_num:
                    grid[y][x] = None

    def is_valid_placement(x, y, size, is_vertical, ship_num):
        # Check if a ship can be placed at the given position
        if is_vertical:
            if y + size > 10:
                return False
            return all(grid[y + i][x] is None or grid[y + i][x] == ship_num for i in range(size))
        else:
            if x + size > 10:
                return False
            return all(grid[y][x + i] is None or grid[y][x + i] == ship_num for i in range(size))

    while not finished:
        screen.fill(WHITE)
        text = font.render(f"Player {player} Ship Placement", True, BLACK)
        screen.blit(text, (350, 20))

        # Draw the grid and label it with letters and numbers
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                pygame.draw.rect(screen, BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)
                if grid[j][i] is not None:  # If a ship is placed, color it dark gray
                    pygame.draw.rect(screen, DARK_GRAY, (50 + i * 50, 100 + j * 50, 50, 50))
                screen.blit(font.render(chr(65 + i), True, BLACK), (65 + i * 50, 70))
                screen.blit(font.render(str(j + 1), True, BLACK), (20, 115 + j * 50))

        # Draw the ships in the sidebar
        for ship in ships:
            pygame.draw.rect(screen, DARK_GRAY, ship)
            if ships.index(ship) == selected:
                pygame.draw.rect(screen, RED, ship, 2)

        # Draw rotate and finish buttons
        rotate_text = "Rotate (V)" if vertical else "Rotate (H)"
        draw_button(rotate_text, 600, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(vertical=not vertical))

        all_ships_placed = all(ship.left < 600 for ship in ships)
        draw_button("Finish", 800, 600, 150, 50, LIGHT_GRAY, lambda: 0, enabled=all_ships_placed)

        # Draw a red outline to show where the selected ship will be placed
        mouse_pos = pygame.mouse.get_pos()
        if selected is not None:
            size = max(ships[selected].width, ships[selected].height) // 50
            if vertical:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size * 50)
            else:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size * 50, 50)
            pygame.draw.rect(screen, RED, indicator, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Use key h or v to rotate
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    vertical = True
                elif event.key == pygame.K_v:
                    vertical = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= event.pos[0] <= 750 and 600 <= event.pos[1] <= 650:
                    vertical = not vertical
                elif 800 <= event.pos[0] <= 950 and 600 <= event.pos[1] <= 650 and all_ships_placed:
                    finished = True
                else:
                    x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                    if 0 <= x < 10 and 0 <= y < 10:
                        if selected is not None:
                            size = max(ships[selected].width, ships[selected].height) // 50
                            if is_valid_placement(x, y, size, vertical, selected + 1):
                                # Place the ship on the grid
                                clear_ship(selected + 1)
                                for i in range(size):
                                    if vertical:
                                        grid[y + i][x] = 'S'  # Mark the ship with 'S'
                                    else:
                                        grid[y][x + i] = 'S'  # Mark the ship with 'S'
                                ships[selected] = pygame.Rect(50 + x * 50, 100 + y * 50, 50 if vertical else size * 50, size * 50 if vertical else 50)
                            selected = None
                        else:
                            # Select a ship that's already on the grid
                            for i, ship in enumerate(ships):
                                if ship.collidepoint(event.pos):
                                    selected = i
                                    break
                    else:
                        # Select a ship from the sidebar or pick up a placed ship
                        for i, ship in enumerate(ships):
                            if ship.collidepoint(event.pos):
                                if ship.left < 600:  # If ship is on the grid
                                    selected = i
                                else:  # If ship is in the sidebar
                                    selected = i
                                    clear_ship(i + 1)
                                break

        pygame.display.flip()

    # Store the completed ship placement for each player
    if player == 1:
        player1_ships = grid
    else:
        player2_ships = grid

def pass_screen(player):
    global finished
    finished = False
    while not finished:
        screen.fill(WHITE)
        text = font.render(f"Pass to player {player}", True, BLACK)
        screen.blit(text, (350, 20))
        draw_button("Finish", 400, 600, 150, 50, LIGHT_GRAY, lambda: 0)
 
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= event.pos[0] <= 550 and 600 <= event.pos[1] <= 650:
                    finished = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def battle_screen(player, opponent_grid, hits_grid):
    global finished
    finished = False
    shot_result = None  # Track if the last shot was a hit or miss
    attack_made = False  # Track if an attack has been made

    while not finished:
        screen.fill(WHITE)
        text = font.render(f"Player {player}: Select a cell to attack", True, BLACK)
        screen.blit(text, (300, 20))

        # Draw the opponent's grid
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                pygame.draw.rect(screen, BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)

                if hits_grid[j][i] == 'M':  # Missed shot
                    pygame.draw.circle(screen, LIGHT_BLUE, (75 + i * 50, 125 + j * 50), 20, 2)
                elif hits_grid[j][i] == 'H':  # Hit shot
                    pygame.draw.line(screen, RED, (60 + i * 50, 110 + j * 50), (90 + i * 50, 140 + j * 50), 3)
                    pygame.draw.line(screen, RED, (90 + i * 50, 110 + j * 50), (60 + i * 50, 140 + j * 50), 3)

        # Show the result of the last shot
        if shot_result:
            result_text = font.render(shot_result, True, BLACK)
            screen.blit(result_text, (400, 650))

        # Draw a "Finish Turn" button
        def on_press():
            global finished
            finished = True
        draw_button("Finish Turn", 800, 600, 150, 50, LIGHT_GRAY, on_press)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not attack_made:
                # Get the grid coordinates the player clicked on
                x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                if 0 <= x < 10 and 0 <= y < 10:
                    # Check if this cell has already been attacked
                    if hits_grid[y][x] is None:
                        if opponent_grid[y][x] == 'S':  # Hit
                            hits_grid[y][x] = 'H'
                            opponent_grid[y][x] = 'H'
                            shot_result = "Hit!"
                        else:  # Miss
                            hits_grid[y][x] = 'M'
                            shot_result = "Miss!"
                        attack_made = True  # Lock out further attacks
                    else:
                        # If the cell has already been attacked, do nothing
                        shot_result = "Already Attacked!"

        pygame.display.flip()
    
    # Check for game over condition
    def all_ships_sunk(grid):
        for row in grid:
            print(row)
            if 'S' in row:  # Check if there are any ships left
                return False
        return True

    if all_ships_sunk(opponent_grid):
        finished = True
        winner = 2 if player == 2 else 1
        return winner  # Return the winner
    else:
        return 0  # Continue the game

def winner_screen(player):
    screen.fill(WHITE)
    text = font.render(f"Player {player} Wins!", True, BLACK)
    screen.blit(text, (350, 200))

    def new_game():
        global game_running, restart_game
        restart_game = True  # Set flag to restart the game
        game_running = False  # Exit the current game loop

    def end_game():
        pygame.quit()
        sys.exit()

    # Draw "New Game" button
    draw_button("New Game", 300, 400, 150, 50, LIGHT_GRAY, action=new_game)

    # Draw "End Game" button
    draw_button("End Game", 500, 400, 150, 50, LIGHT_GRAY, action=end_game)

    # Wait for user interaction
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check button clicks
        if (300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 450) and mouse_pressed[0]:
            new_game()
        elif (500 <= mouse_pos[0] <= 650 and 400 <= mouse_pos[1] <= 450) and mouse_pressed[0]:
            end_game()

        pygame.display.flip()

        if not game_running:
            break

def main():
    global num_ships, player1_ships, player2_ships
    global game_running, restart_game

    restart_game = False  # Flag to restart the game
    game_running = True  # Flag to control game loop

    while True:
        if restart_game:
            # Reset game state for a new game
            num_ships = 0
            player1_ships = None
            player2_ships = None
            main()  # Reset game to start screen
        start_screen()
        # Initialize hits grids for each player
        player1_hits = [[None] * 10 for _ in range(10)]
        player2_hits = [[None] * 10 for _ in range(10)]

        # Player 1 ship placement
        placement_screen(1)
        pass_screen(2)

        # Player 2 ship placement
        placement_screen(2)
        pass_screen(1)

        # Start the battle
        winner = 0
        while winner == 0:
            pass_screen(1)
            winner = battle_screen(1, player2_ships, player1_hits)  # Player 1 attacks Player 2
            if winner:
                break
            
            pass_screen(2)
            winner = battle_screen(2, player1_ships, player2_hits)  # Player 2 attacks Player 1
            if winner:
                break

        # Display winner and wait for user action
        winner_screen(winner)

# Run the main game loop
if __name__ == "__main__":
    main()
