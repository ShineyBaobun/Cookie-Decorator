import pygame
from random import randint

def flour_falling(right,pour,core,image,imagerect,buttons,flour_volume_text,reset,screen,font):
    """
    controls what happends during the flour game
    
    :param right: boolean controlling whether the basket moves left or right
    :param pour: boolean value to determine whether the flour is being poured
    :param core: dictionary of core ingredients
    :param image: image of sieve
    :param imagerect: rect of sieve
    :param complete: image of complete button
    :param completerect: rect of complete button
    :param flour_volume_text: text that displays the volume of flour collected
    :param reset: dictionary of values
    :param screen: surface where images appear
    :param font: font of text
    """
    flour_volume_text = font.render(f"Volume: {core["flour"].achieved_value}", True, "Black")
    screen.blit(image,imagerect)
    cup = pygame.draw.rect(screen, "black", [reset["sieve_x"][1], 400, 300, 300], 10)
    fill = pygame.draw.rect(screen, "white", [reset["sieve_x"][1]+10, reset["sieve_y"][1], 280, reset["sieve_h"][1]])
    buttons["flour_complete"].draw(screen)
    screen.blit(flour_volume_text,(1100,150))

    if right:
        reset["sieve_x"][1] += 5
    else:
        reset["sieve_x"][1] -= 5
    if reset["sieve_x"][1] >= 1000:
        right = False
    if reset["sieve_x"][1] <= 300:
        right = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        pour = True

    if pour and reset["sieve_h"][1] < 290:
        flourfront = pygame.draw.rect(screen, "white", [reset["flour_front_x"][1],imagerect.y + 150,reset["flour_front_w"][1],800])
        flourback = pygame.draw.rect(screen, "white", [imagerect.x + 75,imagerect.y + 150,150, cup.y - imagerect.y + 140])
        if cup.x <= flourback.x + 150 and cup.x +300 >= flourback.x:
            if cup.x > imagerect.x and cup.x < imagerect.x + 225:
                reset["flour_front_w"][1] = cup.x - imagerect.x - 75
                reset["flour_front_x"][1] = imagerect.x + 75
            elif cup.x < imagerect.x and cup.x +300 > imagerect.x + 75:
                reset["flour_front_w"][1] = imagerect.x -75 - cup.x
                reset["flour_front_x"][1] = cup.x + 300
            else:
                reset["flour_front_w"][1] = 150
                reset["flour_front_x"][1] = imagerect.x + 75
            reset["sieve_h"][1]+= abs(cup.y - imagerect.y)/300
            reset["sieve_y"][1]-= abs(cup.y - imagerect.y)/300
            core["flour"].spilled += int(flourfront.width/100)
            core["flour"].achieved_value += int(abs(cup.y - imagerect.y)/100)
            flour_volume_text = font.render(f"Volume: {core["flour"].achieved_value}", True, "Black")
        else:
            core["flour"].spilled += 1

    return right,flour_volume_text

def flour_keys(games,pour,played,reset,event,buttons):
    """
    controls what happens when keys are pressed during the flour game
    
    :param games: dictionary of boolean values
    :param pour: boolean value which shows whether flour is being poured
    :param played: dictionary of boolean vlaues
    :param reset: dictionary of values
    :param event: tracks events that occue
    :completerect: rect of the check mark which ends the flour game
    """
    flour_keys = pygame.key.get_pressed()
    if flour_keys[pygame.K_DOWN]:
        pour = True
    else: 
        pour = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if buttons["flour_complete"].is_clicked(event):
            reset["bowl_color"][1] = (245, 236, 226)
            reset["bowl_r"][1]+= 10
            games["flour_game"] = False
            played["flour_played"] = True
            games["show_minigame"] = False
    return pour
