import pygame
from random import randint

clock = pygame.time.Clock()
fps = 100

pygame.init()

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))

font = pygame.font.Font(None, 30)

class Button:
    def __init__(self,w,h,x,y,image):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w,h))
        self.image_rect = self.image.get_rect(center = (x,y))
    
    def draw(self, surface):
        surface.blit(self.image, self.image_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
level_button = Button(400,100,width/2,height/2 - 50,'assets/minigame.png')
shop_button = Button(400,100,width/2,height/2 +75,'assets/minigame.png')
play_button = Button(400,100,width/2,height/2 +200,'assets/minigame.png')
tutorial_button = Button(400,100,width/2,height/2 +325,'assets/minigame.png')

#Ingredient class and initialization
class Ingredient:
    def __init__(self, path, x, y):
        self.path = path
        self.x = x
        self.y = y
        self.image = pygame.image.load(path)
        self.image_rect = self.image.get_rect(topleft=(x,y))
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    def draw(self, surface):
        surface.blit(self.image, self.image_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
class Core(Ingredient):
    def __init__(self, path, x, y):
        super().__init__(path, x, y)
        self.expected_value = []
        self.achieved_value = []

class Topping(Ingredient):
    def __init__(self, path, x, y):
        super().__init__(path, x, y)
        self.owned = False
        self.added = False

class level:
    def __init__(self,n):
        self.core_ingredients = []
        self.toppings = []
        self.n = n
        self.image = pygame.image.load("assets/minigame.png")
        self.image = pygame.transform.scale(self.image, (100,100))
        self.x = (n%8) * 125 + 312
        self.y = (n//8) * 125 + 178
        self.image_rect = self.image.get_rect(topleft = ((self.x,self.y)))
        if n == 0:
            self.text = font.render(f'Tutorial', True, (0,0,0))
        else:
            self.text = font.render(f'Level {n}', True, (0,0,0))
        self.text_rect = self.text.get_rect(center = (self.image_rect.w/2 +self.x, self.image_rect.h/2 +self.y))

    def draw(self, surface):
        surface.blit(self.image, self.image_rect)
        surface.blit(self.text, self.text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)

completed_levels = {}
levels = {"tutorial": level(0)
          }

#tutorial ingredient amounts
tutorial_ingredients = {"order": Core("assets/order.png",0,0), 
               "butter" : Core("assets/buttertray.png",342,2),
               "eggtray" : Core("assets/eggtray.png",810,0),
               "flour" : Core("assets/flour.png",1275,13),
               "sugar" : Core("assets/sugar.png",1275,320),
               "milk" : Core("assets/milk.png",1275,620)
        }
tutorial_ingredients["eggtray"].expected_value = 2
tutorial_ingredients["milk"].expected_value = 500
tutorial_ingredients["flour"].expected_value = 500
tutorial_ingredients["sugar"].expected_value = 2
tutorial_ingredients["butter"].expected_value = [[550,500],[700,400], [850,500], [1050,600], [800,600]]
levels["tutorial"].core_ingredients.append(tutorial_ingredients["eggtray"])
levels["tutorial"].core_ingredients.append(tutorial_ingredients["milk"])
levels["tutorial"].core_ingredients.append(tutorial_ingredients["flour"])
levels["tutorial"].core_ingredients.append(tutorial_ingredients["sugar"])
levels["tutorial"].core_ingredients.append(tutorial_ingredients["butter"])

current_level = levels["tutorial"]

minigame_image = pygame.image.load('assets/minigame.png')
minigame_image_rect = minigame_image.get_rect(center = (width/2,height/2))
exit_button = Button(55,55,minigame_image_rect.x+27, minigame_image_rect.y+28,'assets/exit.png')

def level_clicking(button,event,minigame,showlevels,leveldict,playing,current):
    if button.is_clicked(event) and not minigame:
        showlevels = True
        minigame = True

    for name, num in leveldict.items():
        if num.clicked(event) and playing:
            current = num
            playing = True

    return showlevels, minigame, playing, current

def homescreen(levelbutton, shop, play, tut, minigame, miniimage, minirect, exit,showlevels,leveldict,completed):
    screen.fill((225, 150, 164))
    levelbutton.draw(screen)
    shop.draw(screen)
    play.draw(screen)
    tut.draw(screen)

    if minigame:
        screen.blit(miniimage,minirect)
        exit.draw(screen)

    if showlevels:
        for name, thislevel in leveldict.items():
            thislevel.draw(screen)

    if len(completed) <= len(leveldict) and len(leveldict) > 0:
        leveldict[len(completed)] = level(len(completed))
        Ingredients = {"order": Core("assets/order.png",0,0), 
               "butter" : Core("assets/buttertray.png",342,2),
               "eggtray" : Core("assets/eggtray.png",810,0),
               "flour" : Core("assets/flour.png",1275,13),
               "sugar" : Core("assets/sugar.png",1275,320),
               "milk" : Core("assets/milk.png",1275,620)
        }
        Ingredients["eggtray"].expected_value = randint(1,5)
        Ingredients["milk"].expected_value = randint(410,550)
        Ingredients["flour"].expected_value = randint(400,690)
        Ingredients["sugar"].expected_value = randint(1,5)
        leveldict[len(completed)].core_ingredients.append(Ingredients["eggtray"])
        leveldict[len(completed)].core_ingredients.append(Ingredients["milk"])
        leveldict[len(completed)].core_ingredients.append(Ingredients["flour"])
        leveldict[len(completed)].core_ingredients.append(Ingredients["sugar"])
        leveldict[len(completed)].core_ingredients.append(Ingredients["butter"])

    return completed, leveldict



running = True
show_minigame = False
show_levels = False
level_playing = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if exit_button.is_clicked(event):
            show_minigame = False
            show_levels = False

        show_levels, show_minigame, level_playing, current_level = level_clicking(level_button,event,show_minigame,show_levels,levels,level_playing,current_level)

    completed_levels, levels = homescreen(level_button, shop_button, play_button, tutorial_button, show_minigame, minigame_image, minigame_image_rect, exit_button,show_levels,levels,completed_levels)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
