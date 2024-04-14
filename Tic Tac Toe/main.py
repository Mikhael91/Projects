import pygame
import time
import math

# Initializing Pygame
pygame.init()

# Size
WIDTH = 500
HEIGHT = 500

# Colors
AZURE = (0, 127, 255)
GREEN_BLUE = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Line Constants
DIF = 300 / 3
THICKNESS = 7

# Creating screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Fonts
letter_font = pygame.font.SysFont("Forque", 85, "bold")
main_font = pygame.font.SysFont("Roboto", 40)
small_text_font = pygame.font.SysFont("Roboto", 25)
opening_font = pygame.font.SysFont("Helvetica", 85)

# Default Tic Tac Toe board
game_board = [["", "", ""],
              ["", "", ""],
              ["", "", ""]]


# Player and restart Display
def display(player, game_state):
    # Texts needed
    player1 = main_font.render("X", True, BLACK)
    player2 = main_font.render("O", True, BLACK)
    choose = small_text_font.render("Choose Player", True, BLACK)
    turns = small_text_font.render(f"{player}'s turn", True, BLACK)
    choose_player_text = main_font.render("CHOOSE PLAYER", True, WHITE)

    # Display
    if game_state:
        screen.blit(choose, (190, 60))
    else:
        screen.blit(turns, (215, 60))

    # Highlights squares
    if player == "X":
        pygame.draw.rect(screen, AZURE, (80, 20, 155, 35))
    else:
        pygame.draw.rect(screen, AZURE, (270, 20, 155, 35))

    # creates a square
    pygame.draw.rect(screen, WHITE, (80, 20, 150, 30))
    pygame.draw.rect(screen, WHITE, (270, 20, 150, 30))

    # Gives text to each box
    screen.blit(player1, (85, 23))
    screen.blit(player2, (275, 23))

    # Creates reset button
    screen.blit(choose_player_text, (135, 440))


# Function to draw Tic Tac Toe grid
def update_window():
    # Insert "X" or "O" in each grid
    for row in range(3):
        for column in range(3):
            if game_board[row][column] == "X":  # 1 = "X"
                text = letter_font.render("X", True, WHITE)
                screen.blit(text, (((column + 1) * DIF) + 26, ((row + 1) * DIF) + 26))
            elif game_board[row][column] == "O":  # 2 = "O"
                text = letter_font.render("O", True, WHITE)
                screen.blit(text, (((column + 1) * DIF) + 26, ((row + 1) * DIF) + 26))

    # Creates the grid
    for lines in range(4):
        if lines % 3 == 0:
            continue
        pygame.draw.line(screen, AZURE, ((lines + 1) * DIF, 100), ((lines + 1) * DIF, 400), THICKNESS)
        pygame.draw.line(screen, AZURE, (100, (lines + 1) * DIF), (400, (lines + 1) * DIF), THICKNESS)


# Restarts the game
def reset():
    for row in range(3):
        for column in range(3):
            game_board[row][column] = ""
    return True


# Checks for blank spaces
def blank_space():
    empty_space = []
    for row in range(3):
        for column in range(3):
            if game_board[row][column] == "":
                empty_space.append((row, column))
    return len(empty_space)


# Checks for winner
def check_winner():
    # Checks rows for wins
    for row in range(3):
        if game_board[row][0] == game_board[row][1] == game_board[row][2] != "":
            return game_board[row][0]

    # Checks columns for wins
    for column in range(3):
        if game_board[0][column] == game_board[1][column] == game_board[2][column] != "":
            return game_board[0][column]

    # Checks diagonals for wins
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != "":
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != "":
        return game_board[0][2]

    # TIE GAME
    if blank_space() == 0:
        return "TIE"
    return None


# Checks for valid moves
def valid_moves(row, column):
    if game_board[row][column] == "":
        return True
    return False


# mouse position
def player_move(x, y, difference):
    row = int((x // difference) - 1)
    column = int((y // difference) - 1)
    return row, column


# computer picks a blank spot
def random_move():
    for row in range(3):
        for column in range(3):
            if valid_moves(row, column):
                return row, column


# Puts a letter in the board
def make_move(player, row, column):
    if valid_moves(row, column):
        game_board[row][column] = player
        return True
    return False


# Checks for possible moves
def possible_moves(board):
    moves = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == "":
                moves.append((row, column))
    return moves


# Evaluate the board value
def evaluate(board, player, opponent):
    # Checks every row
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            if board[row][0] == player:
                return 1 * (1 + blank_space())
            elif board[row][0] == opponent:
                return -1 * (1 + blank_space())

    # Checks every column
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != "":
            if board[0][column] == player:
                return 1 * (1 + blank_space())
            elif board[0][column] == opponent:
                return -1 * (1 + blank_space())

    # Checks all the diagonals
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != "":
        if board[0][0] == player:
            return 1 * (1 + blank_space())
        elif board[0][0] == opponent:
            return -1 * (1 + blank_space())
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != "":
        if board[0][2] == player:
            return 1 * (1 + blank_space())
        elif board[0][2] == opponent:
            return -1 * (1 + blank_space())

    if blank_space() == 0:
        return 0

    return 1 * (1 + blank_space())


# Minimax(Alpha-Beta Pruning) algorithm:
def minimax(board, depth, alpha, beta, maximizing_player, player, opponent):
    if depth == 0 or check_winner():
        return evaluate(board, player, opponent)

    if maximizing_player:
        max_eval = -math.inf
        for row, column in possible_moves(board):
            if valid_moves(row, column):
                board[row][column] = player
                evaluation = minimax(board, depth - 1, alpha, beta, False, player, opponent)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                board[row][column] = ""
                if beta < alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for row, column in possible_moves(board):
            if valid_moves(row, column):
                board[row][column] = opponent
                evaluation = minimax(board, depth - 1, alpha, beta, True, player, opponent)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                board[row][column] = ""
                if beta < alpha:
                    break
        return min_eval


# Computer move
def computer_move(board, player, opponent, depth):
    best_value = -math.inf
    best_move = [-1, -1]
    for row in range(3):
        for column in range(3):
            if valid_moves(row, column):
                board[row][column] = player
                move_value = minimax(board, depth, -math.inf, math.inf, False, player, opponent)
                board[row][column] = ""
                if move_value > best_value:
                    best_value = move_value
                    best_move = [row, column]
    return best_move


# Display difficulty choices and play game choice
def start_display(x, y):
    pygame.draw.rect(screen, WHITE, (175, 200, 150, 35))
    pygame.draw.rect(screen, WHITE, (175, 250, 150, 35))
    pygame.draw.rect(screen, WHITE, (175, 300, 150, 35))
    pygame.draw.rect(screen, WHITE, (175, 350, 150, 35))

    if 175 < x < 325:
        if 200 < y < 235:
            pygame.draw.rect(screen, YELLOW, (175, 200, 150, 35))
        if 250 < y < 285:
            pygame.draw.rect(screen, YELLOW, (175, 250, 150, 35))
        if 300 < y < 335:
            pygame.draw.rect(screen, YELLOW, (175, 300, 150, 35))
        if 350 < y < 385:
            pygame.draw.rect(screen, YELLOW, (175, 350, 150, 35))

    screen.blit(easy_text, (218, 206))
    screen.blit(medium_text, (195, 256))
    screen.blit(impossible_text, (177, 306))
    screen.blit(play_text, (218, 356))
    screen.blit(difficulty_text, (150, 400))


# Variables for game
players = ["X", "O"]
player_index = 0
current_player = "X"
winner = None
game_depth = 0
difficulty = "Easy"

# Game texts
play_again = main_font.render("PLAY AGAIN", True, WHITE)
selected_play_again = main_font.render("PLAY AGAIN", True, AZURE)
selected_choose_player = main_font.render("CHOOSE PLAYER", True, AZURE)
game_title = opening_font.render("TIC TAC TOE", True, WHITE)
easy_text = main_font.render("Easy", True, BLACK)
medium_text = main_font.render("Medium", True, BLACK)
impossible_text = main_font.render("Impossible", True, BLACK)
play_text = main_font.render("Play", True, BLACK)

# Bool variables
game_screen = True
winner_screen = True
start_screen = True
choose_player = True
change_player = False

# Main pygame loop
while True:
    # Resets all variables
    start_screen = True
    game_screen = True
    winner_screen = True
    choose_player = True
    winner = None
    difficulty = "Easy"
    game_depth = 0

    # Start screen loop
    while start_screen:
        # Fills background
        screen.fill(AZURE)

        # Loops through all the events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                quit()

        # Game title
        screen.blit(game_title, (40, 60))

        # Mouse info
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed(num_buttons=3)
        mouse_x, mouse_y = mouse_pos

        # Choosing difficulty and starting game
        if 175 < mouse_x < 325 and mouse_button[0]:
            if 200 < mouse_y < 235:
                game_depth = 0
                difficulty = "Easy"
            if 250 < mouse_y < 285:
                game_depth = 1
                difficulty = "Medium"
            if 300 < mouse_y < 335:
                game_depth = math.inf
                difficulty = "Impossible"
            if 350 < mouse_y < 385:
                start_screen = False

        # Difficulty text
        difficulty_text = main_font.render(f"Difficulty : {difficulty}", True, BLACK)

        # Displaying choices and start game choice
        start_display(mouse_x, mouse_y)

        # Updates pygame screen
        clock.tick(60)
        pygame.display.update()

    # Waits 0.5 seconds before changing screen
    time.sleep(0.5)

    # Main game loop
    while game_screen:
        # Gives background a color
        screen.fill(GREEN_BLUE)

        # Mouse position and buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed(num_buttons=3)
        mouse_x, mouse_y = mouse_pos

        # Loops through events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                quit()

        # Choosing player and main game
        if choose_player:
            current_player = "X"
            player_index = 0
            if 80 < mouse_x < 230 and 20 < mouse_y < 50 and mouse_button[0]:
                player_index = 0
                choose_player = False
            elif 270 < mouse_x < 420 and 20 < mouse_y < 50 and mouse_button[0]:
                player_index = 1
                choose_player = False
            elif 100 < mouse_x < 400 and 100 < mouse_y < 400 and mouse_button[0]:
                choose_player = False
        else:
            # Move
            if current_player == players[player_index]:
                if 100 < mouse_x < 400 and 100 < mouse_y < 400 and mouse_button[0]:
                    position = player_move(mouse_y, mouse_x,  DIF)
                    if make_move(current_player, position[0], position[1]):
                        change_player = True
            else:
                position = computer_move(game_board, current_player, "O" if current_player == "X" else "X", game_depth)
                if make_move(current_player, position[0], position[1]):
                    change_player = True

        # Checks for winner
        winner = check_winner()

        # Displays Players turn
        display(current_player, choose_player)

        # Restarts game
        if 137 < mouse_x < 370 and 442 < mouse_y < 462:
            screen.blit(selected_choose_player, (135, 440))
            underline = pygame.draw.line(screen, AZURE, (137, 468), (370, 468), 3)
            if mouse_button[0]:
                choose_player = reset()

        # Updates window
        update_window()

        # Checks winner
        if winner:
            game_screen = False
            change_player = False

        # Change Player
        if change_player:
            current_player = "O" if current_player == "X" else "X"
            change_player = False

        # Updates pygame screen
        clock.tick(60)
        pygame.display.update()

    # Waits 0.5 seconds before changing screen
    time.sleep(0.5)

    while winner_screen:
        # Fill background color
        screen.fill(GREEN_BLUE)

        # Mouse position and buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed(num_buttons=3)
        mouse_x, mouse_y = mouse_pos

        # Loops through all the events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                quit()

        # Show Winner
        if winner == "TIE":
            game_winner = letter_font.render("DRAW", True, BLACK)
            screen.blit(game_winner, (145, 200))
        else:
            game_winner = letter_font.render(f"{winner} WINS", True, BLACK)
            screen.blit(game_winner, (125, 200))

        # Play again
        screen.blit(play_again, (170, 440))
        if 172 < mouse_x < 338 and 442 < mouse_y < 462:
            screen.blit(selected_play_again, (170, 440))
            underline = pygame.draw.line(screen, AZURE, (172, 468), (338, 468), 3)
            if mouse_button[0]:
                winner_screen = False
                reset()

        # Updates pygame screen
        clock.tick(60)
        pygame.display.update()

