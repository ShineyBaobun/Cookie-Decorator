import pygame
from random import randint

pygame.init()

def add_clicking(adds, games,reset,event):
    """
    controls what happens when different add ins are clicked and added to the cookies
    
    :param adds: dictionary of add ins
    :param games: dictionary of boolean values
    :param reset: dictionary of values
    :param event: tracks the events that occur
    """
    for name, item in adds.items():
        if item.clicked(event): 
            if item.owned and not games["toppings_time"]:
                if name != "food coloring":
                    item.added = True
                    if name == "chocolate chips":
                        reset["bowl_color"][1] = (123,63,0)
                    if name == "sprinkles":
                        reset["bowl_color"][1] = (255,192,203)
                    if name == "oats":
                        reset["bowl_color"][1] = (209,179,153)
                    if name == "peanuts":
                        reset["bowl_color"][1] = (120, 47, 22)
                    if name == "pistachios":
                        reset["bowl_color"][1] = (147, 197, 114)
                    if name == "matcha":
                        reset["bowl_color"][1] = (145, 181, 0)
                    if name == "raisins":
                        reset["bowl_color"][1] = (36, 33, 36)
                if name == "food coloring":
                    games["add_coloring"] = True
            if not item.owned and not games["toppings_time"]:
                games["not_owned_mini"] = True

def top_clicking(tops,games,event):
    """
    controls what happens when different toppings are clicked and added to the cookies
    
    :param tops: dictionary of toppings
    :param games: dictionary of boolean values
    :param event: tracks the events that occur
    """
    for name, item in tops.items():
        if item.clicked(event):
            games["show_minigame"] = False 
            if item.owned:
                if name == "icing":
                    games["add_icing"] = True
                    games["show_minigame"] = True
                else:
                    item.added = True
                    games["show_minigame"] = False
            if not item.owned:
                games["not_owned_mini"] = True

def add_top_draw(adds,tops,games,screen):
    """
    draws different images based on which add ins and toppings were added to the cookes
    
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param games: dictionary of boolean values
    :param screen: surface where images appear
    """
    if games["added_icing"]:
        tops["icing"].added = True
        games["add_icing"] = False
    if not games["show_minigame"]:
        for name, item in adds.items():
            if name != "food coloring" and name!= "matcha" and item.added and games["toppings_time"]:
                screen.blit(item.show_img, (0,0))
        for name, item in tops.items():
            if item.added:
                screen.blit(item.show_img, (0,0))
        if games["not_owned_mini"]:
            games["show_minigame"] = True

def choose_color(colors,games,adds,reset,event,screen):
    """
    stores which color of food coloring was added
    
    :param colors: dictionary of color buttons
    :param games: dictionary of boolean values
    :param adds: dictionary of add ins
    :param reset: dictionary of values
    :param event: tracks the events that occur
    :param screen: surface where images appear
    """
    color_order = ["red", "green", "blue"]
    games["show_minigame"] = True
    for shade, button in colors.items():
        button.draw(screen)
        if button.is_clicked(event):
            adds["food coloring"].achieve_rgb = [0,0,0]
            adds["food coloring"].achieve_rgb[color_order.index(shade)] = 100
            adds["food coloring"].added = True
            reset["cookies"][1].fill(tuple(adds["food coloring"].achieve_rgb), special_flags=pygame.BLEND_RGB_ADD)
            games["add_coloring"] = False
            games["show_minigame"] = False
            reset["bowl_color"][1] = tuple(adds["food coloring"].achieve_rgb)

def choose_icing(colors,games,tops,event,screen):
    """
    stores which color of icing was added to cookies
    
    :param colors: dictionary of color buttons
    :param games: dictionary of boolean values
    :param tops: dictionary of toppings
    :param event: tracks the events that occur
    :param screen: surface where images appear
    """
    color_order = ["red", "green", "blue"]
    games["show_minigame"] = True
    for shade, button in colors.items():
        button.draw(screen)
        if button.is_clicked(event):
            tops["icing"].show_img = tops["icing"].show_img_OG.copy()
            tops["icing"].achieve_rgb = [50,50,50]
            tops["icing"].achieve_rgb[color_order.index(shade)] = 255
            tops["icing"].show_img.fill(tuple(tops["icing"].achieve_rgb), special_flags=pygame.BLEND_RGB_MIN)
            games["added_icing"] = True
            games["show_minigame"] = False
