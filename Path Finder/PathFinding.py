import pygame


class Node:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __getitem__(self, item):
        return self.position[item]


def path_finder(board, start_spot, end_spot):
    # Start and End nodes
    start_node = Node(None, start_spot)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end_spot)
    end_node.g = end_node.h = end_node.f = 0
    # Open and Closed list
    open_list = []
    closed_list = []

    # Adds start node to open list
    open_list.append(start_node)

    # Loops until open list is empty
    while len(open_list) > 0:
        screen.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return
        current_node = open_list[0]
        current_index = 0

        # Finds the node with the smallest f cost
        for index, nodes in enumerate(open_list):
            if nodes.f < current_node.f:
                current_node = nodes
                current_index = index

        # Pops the current node from the open list and adds it to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # If target node has been found
        if current_node == end_node:
            trace_path = []
            while current_node is not None:
                trace_path.append(current_node.position)
                current_node = current_node.parent
            return trace_path, open_list, closed_list

        # Loops through all the neighbours
        for neighbour in get_neighbours(current_node):  # Neighbor nodes
            # If neighbour is out of range
            if (not 0 <= neighbour[0] < len(board)) or (not 0 <= neighbour[1] < len(board[0])):
                continue
            # If neighbour is not traversable
            if board[neighbour[0]][neighbour[1]] == 1:
                continue
            # If neighbour is already in closed list
            if neighbour in closed_list:
                continue
            new_g = current_node.g + get_distance(neighbour, current_node)
            if neighbour in open_list:
                for open_node in open_list:
                    if open_node == neighbour and new_g < open_node.g:
                        open_node.g = new_g
                        open_node.h = get_distance(end_node, neighbour)
                        open_node.f = open_node.g + open_node.h
                        open_node.parent = current_node
            else:
                # Generates neighbour's g, h, and f cost
                neighbour.g = current_node.g + get_distance(neighbour, current_node)
                neighbour.h = get_distance(end_node, neighbour)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.parent = current_node
                # Adds neighbour to open list
                open_list.append(neighbour)
        draw_list(open_list, closed_list)
        draw()
        pygame.display.update()
    return None, None, None


# Gets the distance between two nodes
def get_distance(node_1, node_2):
    dist_row = abs(node_1[0] - node_2[0])
    dist_col = abs(node_1[1] - node_2[1])
    if dist_row > dist_col:
        return 14 * dist_col + (10 * (dist_row - dist_col))
    return 14 * dist_row + (10 * (dist_col - dist_row))


# Finds the neighbours of the current node
def get_neighbours(current_node):
    neighbours = []
    for position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_position = (current_node[0] + position[0], current_node[1] + position[1])
        neighbour_node = Node(None, new_position)
        neighbours.append(neighbour_node)
    return neighbours


def draw():
    for rows in range(number_of_box):
        for column in range(number_of_box):
            if maze[rows][column] == 1:
                pygame.draw.rect(screen, BLACK, (column * dif, rows * dif, dif, dif))
            elif maze[rows][column] == 2:
                pygame.draw.rect(screen, PURPLE, (column * dif, rows * dif, dif, dif))
            elif maze[rows][column] == 3:
                pygame.draw.rect(screen, BLUE, (column * dif, rows * dif, dif, dif))
    for x in range(number_of_box):
        pygame.draw.line(screen, BLACK, (x * dif, 0), (x * dif, SIZE))
    for y in range(number_of_box):
        pygame.draw.line(screen, BLACK, (0, y * dif), (SIZE, y * dif))


def draw_list(list_open, list_closed):
    if list_open is None or list_closed is None:
        return
    for position in list_open:
        x = position[1]
        y = position[0]
        pygame.draw.rect(screen, GREEN, (x * dif, y * dif, dif, dif))
    for position in list_closed:
        x = position[1]
        y = position[0]
        pygame.draw.rect(screen, RED, (x * dif, y * dif, dif, dif))


def draw_path(path_list):
    if path_list is None:
        return
    for position in path_list:
        x = position[1]
        y = position[0]
        pygame.draw.rect(screen, YELLOW, (x * dif, y * dif, dif, dif))


def get_mouse_pos(position):
    row = position[1] // dif
    column = position[0] // dif

    return row, column


# Constants
SIZE = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255)

# Variable
running = True
start = None
end = None
open_nodes = None
closed_nodes = None
path = None
number_of_box = 80
dif = SIZE // number_of_box
maze = [[0 for column in range(number_of_box)] for row in range(number_of_box)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            row, column = get_mouse_pos(mouse_pos)
            spot = (row, column)
            if not start and spot != end:
                start = spot
                maze[row][column] = 2
            elif not end and spot != start:
                end = spot
                maze[row][column] = 3
            elif spot != start and spot != end:
                maze[row][column] = 1
        if pygame.mouse.get_pressed(3)[2]:
            mouse_pos = pygame.mouse.get_pos()
            row, column = get_mouse_pos(mouse_pos)
            if maze[row][column] == 2:
                start = None
            elif maze[row][column] == 3:
                end = None
            maze[row][column] = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                start = None
                end = None
                open_nodes = None
                closed_nodes = None
                path = None
                for row in range(number_of_box):
                    for column in range(number_of_box):
                        maze[row][column] = 0
            if event.key == pygame.K_SPACE:
                if start and end:
                    path, open_nodes, closed_nodes = path_finder(maze, start, end)
    draw_list(open_nodes, closed_nodes)
    draw_path(path)
    draw()
    pygame.display.update()
