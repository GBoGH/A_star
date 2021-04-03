import sys
from queue import PriorityQueue
import random

import pygame
from pygame.locals import *
import pyautogui

from custom import *

pygame.init()

screen_height = 800
screen_width = 800

# Window settings
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A* pathfinder")

# RGB color codes.
black = (0, 0, 0)  # Bariers.
grey = (128, 128, 128)  # Borders.
white = (255, 255, 255)  # Common node.
red = (255, 0, 0)  # Closed node.
green = (0, 255, 0)  # Opened node.
blue = (0, 0, 255)  # End node.
orange = (255, 165, 0)  # Start node.
purple = (255, 0, 255)  # Path.

# Barrier or norder.
borb = [(0, 0, 0), (128, 128, 128)]

# Start, end, path, border.
sepb = [(255, 165, 0), (0, 0, 255), (255, 0, 255), (128, 128, 128)]

# Closed, opened, path.
cop = [(255, 0, 0), (0, 255, 0), (255, 0, 255)]

# Number of rows and columns on the screen. Buggy when changed.
rows = ROWS
cols = COLUMNS

# One in x probability that a node will became barrier in random_barriers().
# 5 is the optimal number.
probability = PROBABILITY


# Creating the Node object.
class Node():
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

    def position(self) -> tuple:
        return self.row, self.col

    """
    Next set of methods either makes the node a certain color or 
    returns the bolean value of the node's color.
    
    """

    def closed_node(self) -> bool:
        return self.color == red

    def make_closed(self) -> None:
        self.color = red

    def opened_node(self) -> bool:
        return self.color == green

    def make_opened(self) -> None:
        self.color = green

    def barrier_node(self) -> bool:
        return self.color == black

    def make_barrier(self) -> None:
        self.color = black

    def start_node(self) -> bool:
        return self.color == orange

    def make_start(self) -> None:
        self.color = orange

    def end_node(self) -> bool:
        return self.color == blue

    def make_end(self) -> None:
        self.color = blue

    def path_node(self) -> bool:
        return self.color == purple

    def make_path(self) -> None:
        self.color = purple

    def border_node(self) -> bool:
        return self.color == grey

    # Method to draw borders around the screen.
    def make_border(self) -> None:
        if self.row == 0 or self.row == self.total_rows-1:
            self.color = grey
        if self.col == 0 or self.col == self.total_cols-1:
            self.color = grey

    # Methods to reset certain nodes.
    def reset(self) -> None:
        self.color = white

    def random_barriers(self, n: int) -> None:
        probability = random.randint(1, n)
        if probability == 1 and self.color not in sepb:
            self.make_barrier()

    def reset_barriers(self) -> None:
        if self.barrier_node():
            self.reset()

    def reset_path(self) -> None:
        if self.color in cop:
            self.reset()

    # Drawing the nodes.
    def draw(self, screen: object) -> None:
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

    # Method for adding neigbour nodes to a list.
    def update_neighbors(self, grid: list) -> None:
        # Down.
        if self.row < self.total_rows - 1 and not \
            (grid[self.row + 1][self.col].barrier_node() or
             grid[self.row + 1][self.col].border_node()):
            self.neighbors.append(grid[self.row+1][self.col])

        # Up.
        if self.row > 0 and not \
            (grid[self.row - 1][self.col].barrier_node() or
             grid[self.row - 1][self.col].border_node()):
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right.
        if self.col < self.total_rows - 1 and not \
            (grid[self.row][self.col + 1].barrier_node() or
             grid[self.row][self.col + 1].border_node()):
            self.neighbors.append(grid[self.row][self.col + 1])

        # left.
        if self.col > 0 and not \
            (grid[self.row][self.col - 1].barrier_node() or
             grid[self.row][self.col - 1].border_node()):
            self.neighbors.append(grid[self.row][self.col - 1])


# Adding all the nodes to a list, creates 2D array of all the class objects.
def create_grid(rows: int, cols: int, width: int, height: int) -> list:
    grid = []
    node_height = height // rows
    node_width = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, node_width, node_height, rows, cols)

            grid[i].append(node)
    return grid


# Creates random barriers according to given probability of node becoming a barrier.
def random_barriers(grid: list, n: int) -> None:
    for row in grid:
        for node in row:
            node.random_barriers(probability)


# Function for drawing all the nodes to the screen.
def draw(screen: object, grid: list) -> None:
    screen.fill(white)
    for row in grid:
        for node in row:
            node.draw(screen)
            node.make_border()

    #draw_grid(screen, rows, cols, screen_width, screen_height)
    pygame.display.update()


def draw_grid(screen: object, rows: int, cols: int, width: int, height: int) -> None:
    node_height = height // rows
    node_width = width // cols

    for i in range(rows):
        pygame.draw.line(screen, black, (0, i*node_height),
                         (width, i * node_height))
        for j in range(cols):
            pygame.draw.line(screen, black, (j*node_width, 0),
                             (j * node_width, height))


# After the path is found, it is drawn
def path(last_node: object, current: object) -> None:
    while current in last_node:
        current = last_node[current]
        current.make_path()
        draw(screen, grid)


# Formula for calculating manhattan (or "L") distance.
def h_score(p1: tuple, p2: tuple) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Function to get position of clicked node.
def get_pos(pos: tuple, rows: int, cols: int, width: int, height: int) -> tuple:
    node_height = height // rows
    node_width = width // cols
    y, x = pos
    row = y // node_height
    col = x // node_width

    return row, col


# A* pathfinding algorithm. Explained in Readme.
def algorithm(grid: list, start: object, end: object) -> bool:
    global finished
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    last_node = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.position(), end.position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]

        open_set_hash.remove(current)

        if current == end:
            path(last_node, end)
            end.make_end()
            start.make_start()

            finished = True
            return finished

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                last_node[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h_score(neighbor.position(), end.position())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_opened()

        draw(screen, grid)

        if current != start:
            current.make_closed()

    return False


# Creating all the nodes
grid = create_grid(rows, cols, screen_width, screen_height)

# Start and end nodes.
start = None
end = None

# Booleans for certain events.
run = True

finished = False
pressed = False

random_select = False

# Main pygame loop.
while run:

    # Pygame event checking.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    # Drawing the grid.
    draw(screen, grid)

    # Checking if mouse if pressed.
    mouse = pygame.mouse.get_pressed()

    # Events after left mouse click.
    if mouse[0]:

        # Get the position of current node.
        pos = pygame.mouse.get_pos()
        row, col = get_pos(pos, rows, cols, screen_width, screen_height)
        node = grid[row][col]

        # If node is not border, create start, end and then barriers.
        if node.border_node():
            pass
        elif not node.border_node():
            # You cannot place start and end on the same node.
            if not start and node != end:
                start = node
                start.make_start()

            elif not end and node != start:
                end = node
                end.make_end()

            elif node != end and node != start:
                node.make_barrier()

    # Events after right mouse click.
    elif mouse[2]:

        # Get the position of the clicked node.
        pos = pygame.mouse.get_pos()
        row, col = get_pos(pos, rows, cols, screen_width, screen_height)
        node = grid[row][col]

        # If node is not border, erase current node.
        if node.border_node():
            pass

        elif not node.border_node():
            node.reset()
            if node == start:
                start = None

            elif node == end:
                end = None

    # Check for key presses.
    key = pygame.key.get_pressed()

    # Start the alghoritm if start and end is given.
    if key[K_RETURN] and start and end:
        for row in grid:
            for node in row:
                if node.color in cop:
                    node.reset()
                node.neighbors.clear()
                # Generate neighbors for every node.
                node.update_neighbors(grid)

        # Start the alghoritm
        algorithm(grid, start, end)

    # Events after the alghoritm is finished.
    if finished:
        # The pop-up display. Also displays only once.
        if not pressed:
            r = "Press P to clear path, open and closed nodes"
            b = "Press B to clear only barriers"
            c = "Press C to clear everything"
            pyautogui.alert(f"{r}\n{b}\n{c}")
        pressed = True
        finished = False

     # Randomly generate barriers. Do only once.
    if key[K_r] and not random_select:
        random_barriers(grid, probability)
        random_select = True

    # Reset everything.
    if key[K_c]:
        start = None
        end = None
        grid = create_grid(rows, cols, screen_width, screen_height)

    # Reset only barriers.
    if key[K_b]:
        for row in grid:
            for node in row:
                node.reset_barriers()
        # If barriers are reset, random generation is re-enabled.
        random_select = False

    # Reset path, opened and closed nodes.
    if key[K_p]:
        for row in grid:
            for node in row:
                if not node.border_node():
                    node.reset_path()
