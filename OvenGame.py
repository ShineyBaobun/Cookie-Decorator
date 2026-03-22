import pygame
from random import randint

pygame.init()

def oven_draw(image,image_rect,reset,games,buttons,screen):
    """
    controls what is drawn during the oven game
    
    :param image: image of oven
    :param image_rect: rect of oven
    :param reset: dictionary of values
    :param games: dictionary of boolean values
    :param buttons: dictionary of buttons
    :param screen: surface where images appear
    """
    screen.fill((225, 150, 164))
    screen.blit(image,image_rect)
    buttons["home"].draw(screen)
    oven_ready_bar = pygame.draw.rect(screen, (reset["oven_r"][1],reset["oven_g"][1],reset["oven_b"][1]),[270,111,reset["oven_width"][1], 88])
    if games["startbutton_show"]:
        buttons["startbutton"].draw(screen)
    elif games["oven_playing"]:
        buttons["stopbutton"].draw(screen)
        if reset["oven_width"][1]<472:
            reset["oven_width"][1] += 1
            if reset["oven_r"][1] > 0 and reset["oven_b"][1] > 0:
                reset["oven_r"][1] -= 0.5
                reset["oven_b"][1] -= 0.5
        elif reset["oven_r"][1] < 255 and reset["oven_g"][1]>0:
            reset["oven_r"][1] += 2
            reset["oven_g"][1] -=2
    else:
        buttons["next"].draw(screen)

def oven_clicking(games,played,buttons,event):
    """
    controls what happens during clicking in the oven game
    
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param buttons: dictionary of buttons
    :param event: tracks the events that occur
    """
    if event.type == pygame.MOUSEBUTTONDOWN:

        if buttons["startbutton"].is_clicked(event) and not played["oven_played"] and games["startbutton_show"]:
            games["clicked_button"] = True
            games["startbutton_show"] = False
            games["oven_playing"] = True
        
        elif buttons["stopbutton"].is_clicked(event) and games["oven_playing"] and not games["clicked_button"]:
            played["oven_played"] = True
            games["oven_playing"] = False

    if event.type == pygame.MOUSEBUTTONUP:
        if buttons["startbutton"].is_clicked_up(event):
            games["clicked_button"] = False
