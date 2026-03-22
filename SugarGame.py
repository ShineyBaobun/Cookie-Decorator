import pygame
from random import randint
from EggGame import basket_update

pygame.init()

class SugarSalt:
    """
    class for the sugar and salts
    """
    def __init__(self, y, type, x):
        """
        Attributes:
        
        :param self: allows class attributes to be accessed
        :param y: y coordinate of object
        :param type: sugar or salt
        :param x: x coordinate of object
        """
        self.x = x
        self.y = y
        self.type = type
        if self.type == "sugar":
            self.image = pygame.image.load('assets/sugarimage.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (75,75))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.type == "salt":
            self.image = pygame.image.load('assets/salt.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (75,100))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, surface):
        """
        draws bottle
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        surface.blit(self.image, self.rect)

    def update(self):
        """
        updates position of the sugars/salts
        
        :param self: allows class attributes to be accessed
        """
        self.rect.y += 4

def sugar_keys(rect,container,basket_dict):
    """
    controls what happens when keys are pressed during the sugar game
    
    :param rect: rect of the basket
    :param container: image of basket
    :param basket_dict: a dictionary that contains rects of all four sides of the basket
    """
    sugar_keys = pygame.key.get_pressed()
    if sugar_keys[pygame.K_LEFT] and rect.x != 1600/2-(container.get_width()/2)-400:
        rect.x -= 400
    if sugar_keys[pygame.K_RIGHT] and rect.x != 1600/2-(container.get_width()/2)+400:
        rect.x += 400
    basket_update(rect, basket_dict)

def sugar_salt_coordinates(reset):
    """
    calculates the coordinates/column of each row of sugar and salt
    
    :param reset: dictionary of values
    """
    reset["SugarSalts"][1] = []
    for i in range(5):
        nums = [375,1600/2-37,1150]
        chosen_x = nums[randint(0,2)]
        reset["SugarSalts"][1].append(SugarSalt(-50-(i*300),"sugar",chosen_x))
        nums.remove(chosen_x)
        chosen_x = nums[randint(0,1)]
        reset["SugarSalts"][1].append(SugarSalt(-50-(i*300),"salt", chosen_x))

def sugar_controls(basket_dict,games,played,core,sugarstext,saltstext,reset,font,screen,basket,basketrect):
    """
    controls what happens during collisions and what is drawn during the sugar game
    
    :param basket_dict: a dictionary that contains rects of all four sides of the basket
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param core: dictionary of core ingredients
    :param sugarstext: text that displays how many sugars have been collected
    :param saltstext: text that displays how many salts have been collected
    :param reset: dictionary of values
    :param font: font of text
    :param screen: surface where images appear
    :param basket: image of basket
    :param basket_rect: rect of basket
    """
    saltstext = font.render(f"Salt Collected: {core["sugar"].achieved_value[1]}", True, "Black")
    sugarstext = font.render(f"Sugar Collected: {core["sugar"].achieved_value[0]}", True, "Black")
    for ingredient in reset["SugarSalts"][1]:
        ingredient.update()
        if ingredient.rect.colliderect(basket_dict["top"]) and ingredient.x >= basket_dict["left"].x and ingredient.x <= basket_dict["right"].x and ingredient.type == "sugar":        
            core["sugar"].achieved_value[0] += 1
            reset["SugarSalts"][1].remove(ingredient)
            sugarstext = font.render(f"Sugar Collected: {core["sugar"].achieved_value[0]}", True, "Black")
        if ingredient.rect.colliderect(basket_dict["top"]) and ingredient.x >= basket_dict["left"].x and ingredient.x <= basket_dict["right"].x and ingredient.type == "salt":        
            reset["SugarSalts"][1].remove(ingredient)
            core["sugar"].achieved_value[1] += 1
            saltstext = font.render(f"Salt Collected: {core["sugar"].achieved_value[1]}", True, "Black")
        if ingredient.rect.y >= 900:
            reset["SugarSalts"][1].remove(ingredient)

    for ingredient in reset["SugarSalts"][1]:
        ingredient.draw(screen)
    screen.blit(basket, basketrect)

    screen.blit(sugarstext,(950,150))
    screen.blit(saltstext,(950,200))

    if not reset["SugarSalts"][1]:
        reset["bowl_color"][1] = (255, 255, 255)
        reset["bowl_r"][1] += 10
        games["sugar_game"] = False
        played["sugar_played"] = True
        games["show_minigame"] = False

    return sugarstext,saltstext
