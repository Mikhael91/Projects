import pygame
import copy

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((630, 700))

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
DIF = 70

# Variables
running = True
fill = False
board_row = 0
board_column = 0
number = 0

# Fonts
font_1 = pygame.font.SysFont("Forque", 60)
font_2 = pygame.font.SysFont("Forque", 25)

# Texts
solve_text = font_2.render("Press 'S' to solve", True, BLACK)
custom_text = font_2.render("Press 'C' for custom board", True, BLACK)
default_text = font_2.render("Press 'D' for default board", True, BLACK)
wait_text = font_2.render("Solving Sudoku...", True, BLACK)

# Game Board
original_sudoku = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                   [5, 2, 0, 0, 0, 0, 0, 0, 0],
                   [0, 8, 7, 0, 0, 0, 0, 3, 1],
                   [0, 0, 3, 0, 1, 0, 0, 8, 0],
                   [9, 0, 0, 8, 6, 3, 0, 0, 5],
                   [0, 5, 0, 0, 9, 0, 6, 0, 0],
                   [1, 3, 0, 0, 0, 0, 2, 5, 0],
                   [0, 0, 0, 0, 0, 0, 0, 7, 4],
                   [0, 0, 5, 2, 0, 6, 3, 0, 0]]
custom_sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
sudoku_display = copy.deepcopy(original_sudoku)


# Draws the sudoku board in pygame
def display_board(board, font):
    for x_line in range(10):
        if x_line % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (x_line * DIF, 0), (x_line * DIF, 630), thickness)
    for y_line in range(10):
        if y_line % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (0, y_line * DIF), (630, y_line * DIF), thickness)
    for row in range(9):
        for column in range(9):
            if board[row][column] != 0:
                text = font.render(str(board[row][column]), True, BLACK)
                screen.blit(text, ((column * DIF) + 27, (row * DIF) + 25))


def valid_move(board, row, column, num):
    # Checks the board horizontally
    for x_pos in range(9):
        if x_pos == column:
            continue
        if board[row][x_pos] == num:
            return False
    # Checks the board vertically
    for y_pos in range(9):
        if y_pos == row:
            continue
        if board[y_pos][column] == num:
            return False
    # Checks the board in a 3x3 region
    start_x = column - column % 3
    start_y = row - row % 3
    for y_pos in range(start_y, start_y + 3):
        for x_pos in range(start_x, start_x + 3):
            if y_pos == row and x_pos == column:
                continue
            if board[y_pos][x_pos] == num:
                return False
    # Valid Move
    return True


def solve_sudoku(board, row, column, diff):
    # Stops the backtracking algorithm we have reached the end of the board
    if row == 8 and column > 8:
        return True
    # If column is bigger than 8, go to next row
    if column > 8:
        row = row + 1
        column = 0
    # If board at index row and column already has a number, go to next column
    if board[row][column] > 0:
        return solve_sudoku(board, row, column + 1, diff)
    # Tries every number
    for num in range(1, 10):
        if valid_move(board, row, column, num):
            # Inserts the number if it is a valid number
            board[row][column] = num
            # Draws a square to visualize board
            screen.fill(WHITE)
            pygame.draw.rect(screen, LIGHT_BLUE, (column * diff, row * diff, diff, diff))
            display_board(sudoku_display, font_1)
            screen.blit(wait_text, (240, 650))
            pygame.display.update()
            pygame.time.delay(20)
            if solve_sudoku(board, row, column + 1, diff):
                return True
            # Backtracks if it fails
            board[row][column] = 0
            screen.fill(WHITE)
            pygame.draw.rect(screen, LIGHT_BLUE, (column * diff, row * diff, diff, diff))
            display_board(sudoku_display, font_1)
            screen.blit(wait_text, (240, 650))
            pygame.display.update()
            pygame.time.delay(20)
    return False


# Main Pygame loop
while running:
    # Loops through all events
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            running = False
        if action.type == pygame.KEYDOWN:
            # Solves board
            if action.key == pygame.K_s:
                solve_sudoku(sudoku_display, 0, 0, DIF)
            # Default board or Custom board
            if action.key == pygame.K_d:
                sudoku_display = copy.deepcopy(original_sudoku)
            if action.key == pygame.K_c:
                sudoku_display = copy.deepcopy(custom_sudoku)
            # Moves Square
            if action.key == pygame.K_UP:
                board_row = board_row - 1 if board_row > 0 else board_row
                number = sudoku_display[board_row][board_column]
            if action.key == pygame.K_DOWN:
                board_row = board_row + 1 if board_row < 8 else board_row
                number = sudoku_display[board_row][board_column]
            if action.key == pygame.K_LEFT:
                board_column = board_column - 1 if board_column > 0 else board_column
                number = sudoku_display[board_row][board_column]
            if action.key == pygame.K_RIGHT:
                board_column = board_column + 1 if board_column < 8 else board_column
                number = sudoku_display[board_row][board_column]
            # Number input
            if action.key == pygame.K_1:
                number = 1
                fill = True
            if action.key == pygame.K_2:
                number = 2
                fill = True
            if action.key == pygame.K_3:
                number = 3
                fill = True
            if action.key == pygame.K_4:
                number = 4
                fill = True
            if action.key == pygame.K_5:
                number = 5
                fill = True
            if action.key == pygame.K_6:
                number = 6
                fill = True
            if action.key == pygame.K_7:
                number = 7
                fill = True
            if action.key == pygame.K_8:
                number = 8
                fill = True
            if action.key == pygame.K_9:
                number = 9
                fill = True

    # Screen background
    screen.fill(WHITE)
    if valid_move(sudoku_display, board_row, board_column, number) or number == 0:
        pygame.draw.rect(screen, LIGHT_BLUE, (board_column * DIF, board_row * DIF, DIF, DIF))
    else:
        pygame.draw.rect(screen, RED, (board_column * DIF, board_row * DIF, DIF, DIF))

    # Display sudoku board
    display_board(sudoku_display, font_1)

    # Gets position of mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed(3)
    if 0 < mouse_pos[0] < 630 and 0 < mouse_pos[1] < 630:
        mouse_row, mouse_column = mouse_pos[1] // DIF, mouse_pos[0] // DIF
        # Draw Square Lines at mouse position
        for x in range(2):
            pass
            pygame.draw.line(screen, RED, (mouse_column * DIF, (mouse_row + x) * DIF),
                             ((mouse_column + 1) * DIF, (mouse_row + x) * DIF), 5)
        for y in range(2):
            pass
            pygame.draw.line(screen, RED, ((mouse_column + y) * DIF, mouse_row * DIF),
                             ((mouse_column + y) * DIF, (mouse_row + 1) * DIF), 5)
        # Draw Square at mouse position
        if mouse_button[0]:
            board_row, board_column = mouse_row, mouse_column
            number = sudoku_display[board_row][board_column]

    # Fills the board with number
    if fill:
        sudoku_display[board_row][board_column] = number
        fill = False

    # Texts
    screen.blit(solve_text, (10, 650))
    screen.blit(default_text, (170, 650))
    screen.blit(custom_text, (410, 650))

    # Updates pygame display
    pygame.display.update()
