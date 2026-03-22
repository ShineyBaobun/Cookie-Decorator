import pygame
from random import randint

width = 1600
height = 900

pygame.init()

def egg_collisions(egg_list,basket_dict,core,games,played,text,reset,screen,font):
    """
    tracks if eggs collide with basket and controls how eggs move within the basket and outside it
    
    :param egg_list: list od eggs
    :param basket_dict: a dictionary that contains rects of all four sides of the basket
    :param core: dictionary of core ingredients
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param text: text that displays number of eggs collected
    :param reset: dictionary of values
    :param screen: surface where images appear
    :param font: font of text
    """
    text = font.render(f"Eggs: {core["eggs"].achieved_value}", True, (0,0,0))
    for egg in egg_list:
        egg.update() 
        if egg.rect.colliderect(basket_dict["left"]) and egg.rect.x > basket_dict["left"].x:
            egg.rect.x = basket_dict["left"].x + 10
        if egg.rect.colliderect(basket_dict["left"]) and egg.rect.x <= basket_dict["left"].x:
            egg.rect.x = basket_dict["left"].x-50
        if egg.rect.colliderect(basket_dict["right"]) and egg.rect.x < basket_dict["right"].x:
            egg.rect.x = basket_dict["right"].x -50
        if egg.rect.colliderect(basket_dict["right"]) and egg.rect.x > basket_dict["right"].x:
            egg.rect.x = basket_dict["right"].x + 11
        if egg.rect.colliderect(basket_dict["bottom"]):        
            egg.rect.y = basket_dict["bottom"].y -75
        if egg.rect.colliderect(basket_dict["top"]) and not egg.collected:        
            core["eggs"].achieved_value += 1
            text = font.render(f"Eggs: {core["eggs"].achieved_value}", True, (0,0,0))
            egg.collected = True
            reset["egg_fallen"][1] += 1
        if egg.rect.top >= 900 and not egg.fallen:
            egg.fallen = True
            reset["egg_fallen"][1] += 1
        
        if reset["egg_fallen"][1] == 5:
            reset["bowl_color"][1] = (255, 210, 0)
            reset["bowl_r"][1] += 10
            games["eggs_game"] = False
            played["eggs_played"] = True
            games["show_minigame"] = False

        screen.blit(text,(1100,150))
    return text

def basket_update(rect,basket_dict):
    """
    updates the position of the basket
    
    :param rect: the rect of basket as a whole
    :param basket_dict: a dictionary that contains rects of all four sides of the basket
    """
    basket_dict["bottom"].update(rect.x, rect.y+rect.height-10, rect.width, 10)
    basket_dict["left"].update(rect.x, rect.y, 10, rect.height)
    basket_dict["right"].update(rect.x+rect.width-10, rect.y, 10, rect.height)
    basket_dict["top"].update(rect.x+10, rect.y, rect.width-20, 10)
    
def egg_controls(basket,basketrect,basket_dict,egglist,screen):
    """
    controls what happens when keys are pressed in the egg game
    
    :param basket: the image of the basket
    :param basketrect: the rect of the basket
    :param basket_dict: a dictionary that contains rects of all four sides of the basket
    :param egglist: list of eggs
    :param screen: surface where images appear
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basketrect.x > 256:
        basketrect.x -= 9
    if keys[pygame.K_RIGHT] and basketrect.x < 1344 - basketrect.width:
        basketrect.x += 9
    basket_update(basketrect, basket_dict)

    screen.blit(basket, basketrect)

    for egg in egglist:
        egg.draw(screen)
