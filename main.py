import pygame


pygame.init()

screen_height = 800
screen_width = 800

screen = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0) # barier
white = (255,255,255) # basic node
red = (255, 0, 0) # closed
green = (0, 255, 0) # opened
blue = (0, 0, 255) # finish
yellow = (255, 255, 0) # start
purple = (255, 0, 255) # path


class Node():
    def __init__(self, row, col, width, height, total):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.height = height
        self.total = total

    def position(self):
        return (self.row, self.col)

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
        return self.color == yellow

    def make_start(self):
        self.color = yellow

    def end_node(self):
        return self.color == blue

    def make_end(self):
        self.color = blue

    def path(self):
        self.color = purple

    def reset(self):
        return self.color == white

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def create_grid(rows, cols, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append(rows)
        for j in range(cols):
            node = Node(i, j, gap, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(screen, rows, cols, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(screen, black, (0, i * gap), (width, i * gap))

        for j in range(cols):
            pygame.draw.line(screen, black, (j * gap, 0), (j * gap, 0))

def draw(screen, grid, rows, cols, width):
    screen.fill(white)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, cols, width)

def get_pos(pos, rows, cols, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
