import pygame

pygame.init()

screen_height = 800
screen_width = 800

screen = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
weird_blue = (102, 151, 146)
purple = (255, 0, 255)


class Nodes():
    def __init__(self, row, col, width, total):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total = total

    def position(self):
        return (self.row, self.col)

    def closed_node(self):
        return self.color == red

    def opened_node(self):
        return self.color == green

    def barrier_node(self):
        return self.color == black

    def start_node(self):
        return self.color == weird_blue

    def end_node(self):
        return True

    def reset(self):
        return self.color == white