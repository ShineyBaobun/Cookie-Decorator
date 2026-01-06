import pygame

pygame.init()

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))

# initialize images for all of the cookies and toppings
sprinkles = pygame.image.load('assets/sprinkles.webp')

class Cookie:

    def __init__(self, color, chosen, size, x, y):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0,0,0,0)
        chosen = 'w'
        self.ingredients = []
        self.toppings = []

    def coloring(self, chosen):
        if chosen == 'w':
            self.color = (0,0,0,0)
        if chosen == 'r':
            self.color = (125,50,0,0)
        if chosen == 'b':
            self.color = (0,80,200,0)
        if chosen == 'g':
            self.color = (0,125,50,0)
        if chosen == 'pu':
            self.color = (0,0,125,0)
        if chosen == 'pi':
            self.color = (75,0,125,0)

    def draw(self,screen):
        plain = pygame.image.load('assets/cookie.webp')

class Button:

    def __init__(self, w, h, x, y):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        rect = pygame.Rect(self.x,self.y,self.w,self.h)

    def is_clicked(self):
        pass


#initialize buttons for start, home, levels, and shop

class Ingredient:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

running = True

while running:
    pass

