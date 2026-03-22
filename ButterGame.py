import pygame
from random import randint

pygame.init()

def shoelace(vertices):
    """
    calculates the area between a complete polygon of coordinates
    
    :param vertices: a list of verticies (coordinates)
    """
    total = 0
    for i in range(len(vertices)):
        butter_xy = vertices[i%len(vertices)][0]*vertices[(1+i)%len(vertices)][1]
        butter_yx = vertices[i%len(vertices)][1]*vertices[(1+i)%len(vertices)][0]
        total += butter_xy-butter_yx
    return abs(total)

def butter_clicking(core,back,games,text,event,font):
    """
    controls what happens during clicking in the butter game
    
    :param core: dictionary of core ingredients
    :param back: rect of the back of butter
    :param games: dictionary of boolean values
    :param text: text that displays the volume of butter cut
    :param event: tracks what events have occured
    :param font: 
    """
    if len(core["butter"].achieved_value)<=4:
        mouse_pos = event.pos
        if back.collidepoint(mouse_pos) and not games["clicked_button"]:
            core["butter"].achieved_value.append(pygame.mouse.get_pos())

    text = font.render(f"Current volume: {int(shoelace(core["butter"].achieved_value)/1000)}", True, "black")
    return text

def butter_drawing(games,played,fallen,text,core,reset,screen,butterback):
    """
    determines what is drawn during the butter game
    
    :param current: current level
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param fallen: rect of fallen butter
    :param text: text that displays the volume of butter that has been cut
    :param core: dictionary of core ingredients
    :param reset: dictionary of values
    """
    for i in range(5):
        pygame.draw.line(screen, "green", (core["butter"].expected_value[i%5][0],core["butter"].expected_value[i%5][1]),(core["butter"].expected_value[(i+1)%5][0],core["butter"].expected_value[(i+1)%5][1]),10)
    for i in range(len(core["butter"].achieved_value)):
        pygame.draw.circle(screen,"black",core["butter"].achieved_value[i],2)
        if len(core["butter"].achieved_value) >= 2:
            pygame.draw.line(screen, "black", core["butter"].achieved_value[i%(len(core["butter"].achieved_value))],core["butter"].achieved_value[(i+1)%len(core["butter"].achieved_value)],5)

    if len(core["butter"].achieved_value) == 5 and not fallen:
        fallen = [list(x) for x in core["butter"].achieved_value]

    if len(core["butter"].achieved_value) == 5:
        reset["bowl_color"][1] = (255, 253, 116)
        pygame.draw.polygon(screen,(200,200,200),fallen)
        pygame.draw.polygon(screen,(255, 253, 116),core["butter"].achieved_value)
        for i in range(5):
            fallen[i][1] += 5
            core["butter"].expected_value[i][1] += 5
        reset["butter_back_y"][1] += 5

    if butterback.y >= 900:
        games["butter_game"] = False
        played["butter_played"] = True
        games["show_minigame"] = False

    screen.blit(text,(950,150))
    
    return fallen
