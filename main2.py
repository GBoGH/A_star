import sys

import pygame

pygame.init()

def create_grid(i, j):
    node = pygame.Surface(20, 20)
    node_rect = node.get_rect(topleft=(i * 20, j * 20))
    return node_rect









screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A star pathfinding")

black = (0, 0, 0) # barier
white = (255,255,255) # basic node
red = (255, 0, 0) # closed
green = (0, 255, 0) # opened
blue = (0, 0, 255) # finish
yellow = (255, 255, 0) # start
purple = (255, 0, 255)  # path


rows = 50
cols = rows
node_size = screen_height // rows

nodes = []

screen.fill(white)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    for i in range(rows):
        nodes.append([])
        for j in range(cols):
            nodes[i].append(create_grid(i,j))

    pygame.display.update()

print(nodes)