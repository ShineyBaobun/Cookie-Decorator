import pygame
from random import randint

pygame.init()

class Bottle:
    """
    class for bottle
    """
    def __init__(self, x, y, w, h):
        """
        Attributes:
        
        :param self: allows class attributes to be accessed
        :param x: x coordinate of bottle
        :param y: y coordinate of bottle
        :param w: width of bottle
        :param h: height of bottle

        image (image): image of botth
        turned (bool): stores whether the bottle has been turned
        poured (bool): stores whether the bottle has poured milk
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load('assets/milk.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect(center=(x,y))
        self.turned = False
        self.poured = False

    def draw(self, surface):
        """
        draws bottle
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        surface.blit(self.image, self.rect)

    def clicked(self, event):
        """
        checks if button is clicked down
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def clickedup(self,event):
        """
        checks if button is clicked up
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos)

    def toggle_rotation(self):
        """
        rotates the bottle
        
        :param self: allows class attributes to be accessed
        """
        self.turned = not self.turned
        angle = 45 if self.turned else -45
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

def milk_clicking(can,event):
    """
    controls what happens during clicking in the milk game
    
    :param can: the milk can (object of bottle class)
    :param event: tracks the events which occur
    """
    if can.clicked(event):
        can.toggle_rotation()
        if not can.poured and can.turned:
            can.poured = True

def milk_game_controls(can,core,games,played,text,reset,font,screen):
    """
    controls what is drawn during the milk game
    
    :param can: object from the bottle class
    :param core: dictionary of core ingredients
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param text: text that displays the volume of milk collected
    :param reset: dictionary of values
    :param font: font of text
    :param screen: surface where images appear
    """
    text = font.render(f"Volume: {core["milk"].achieved_value}", True, "Black")
    can.draw(screen)
    milk_cup = pygame.draw.rect(screen, "black", [700, 400, 300, 300], 10)
    milk_fill = pygame.draw.rect(screen, "white", [710, reset["milk_y"][1], 280, reset["milk_h"][1]])
    
    if can.turned:
        milk_liquid = pygame.draw.rect(screen, "white", [840,213,10,477])
        reset["milk_h"][1]+=1
        reset["milk_y"][1]-=1
        core["milk"].achieved_value += 1
        text = font.render(f"Volume: {core["milk"].achieved_value}", True, "Black")

    if can.turned and core["milk"].achieved_value >= 230:
        can.toggle_rotation()
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    if not can.turned and can.poured:
        reset["bowl_r"][1] += 10
        reset["bowl_color"][1] = (253, 255, 246)
        can.poured = False
        can.turned = False
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    screen.blit(text, (1100,150))

    return text
