import sys
from queue import PriorityQueue

import pygame
from pygame.locals import *

pygame.init()

screen_height = 800
screen_width = 800

screen = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0)  # barier
grey = (128,128,128)
white = (255, 255, 255)  # basic node
red = (255, 0, 0)  # closed
green = (0, 255, 0)  # opened
blue = (0, 0, 255)  # finish
orange = (255, 165, 0)  # start
purple = (255, 0, 255)  # path

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

    def position(self):
        return self.row, self.col

    def closed_node(self):
        return self.color == red

    def make_closed(self):
        self.color = red

    def opened_node(self):
        return self.color == green

    def make_opened(self):
        self.color = green

    def barrier_node(self):
        return self.color == black

    def make_barrier(self):
        self.color = black

    def start_node(self):
        return self.color == orange

    def make_start(self):
        self.color = orange

    def end_node(self):
        return self.color == blue

    def make_end(self):
        self.color = blue

    def path(self):
        self.color = purple

    def reset(self):
        self.color = white

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down.
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier_node():
            self.neighbors.append(grid[self.row+1][self.col])

        # Up.
        if self.row > 0 and not grid[self.row - 1][self.col].barrier_node():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier_node():
            self.neighbors.append(grid[self.row][self.col + 1])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].barrier_node():
            self.neighbors.append(grid[self.row][self.col - 1])


def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def path(last_node, current, draw):
    while current in last_node:
        current = last_node[current]
        current.path()
        draw(screen, grid, rows, cols, screen_width, screen_height)

def borders(gird):
    for row in grid:
        for node in row:
            if row == grid[0] or row == grid[-1]:
                node.make_barrier()
            if node == row[0] or node == row[-1]:
                node.make_barrier()

def is_border(row, col):
    if row == 0 or row == rows-1:
        return True
    elif col == 0 or col == cols-1:
        return True
    else:
        return False

def algorithm(grid, start, end):
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
            path(last_node, end, draw)
            end.make_end()
            start.make_start()
            return True

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

        draw(screen, grid, rows, cols, screen_width, screen_height)

        if current != start:
            current.make_closed()

    return False


def create_grid(rows, cols, width, height):
    grid = []
    node_height = height // rows
    node_width = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, node_width, node_height, rows, cols)
            grid[i].append(node)
    return grid

def draw(screen, grid, rows, cols, width, height):
    screen.fill(white)
    for row in grid:
        for node in row:
            node.draw(screen)
    borders(grid)
    pygame.display.update()


def get_pos(pos, rows, cols, width, height):
    node_height = height // rows
    node_width = width // cols
    y, x = pos
    row = y // node_height
    col = x // node_width

    return row, col


rows = 50
cols = 50

grid = create_grid(rows, cols, screen_width, screen_height)

start = None
end = None

run = True
started = False


while run:
    draw(screen, grid, rows, cols, screen_width, screen_height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    mouse = pygame.mouse.get_pressed()

    if mouse[0]:
        pos = pygame.mouse.get_pos()
        row, col = get_pos(pos, rows, cols, screen_width, screen_height)
        node = grid[row][col]

        if is_border(row, col):
            pass
        elif not is_border(row, col):
            if not start and node != end :
                start = node
                start.make_start()

            elif not end and node != start:
                end = node
                end.make_end()

            elif node != end and node != start:
                node.make_barrier()

    elif mouse[2]:
        pos = pygame.mouse.get_pos()
        row, col = get_pos(pos, rows, cols, screen_width, screen_height)

        if is_border(row, col):
            pass

        elif not is_border(row, col):
            node = grid[row][col]
            node.reset()

            if node == start:
                start = None

            elif node == end:
                end = None

    key = pygame.key.get_pressed()

    if key[K_RETURN] and start and end:
        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        algorithm(grid, start, end)

    if key[K_c]:
        start = None
        end = None
        grid = create_grid(rows, cols, screen_width, screen_height)
