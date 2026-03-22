import pygame
from random import randint
import copy
from SugarGame import sugar_salt_coordinates
from ButterGame import shoelace

class Ingredient:
    """
    A class to represent an ingredient

    Attributes:
        path (str): The path to an image.
        x (int): the x-coordinate that determines where the image is placed.
        y (int): the y-coordinate that determines where the image is placed.
        rw (int): the resize width to resize image if needed.
        rh (int): the resize height to resize image if needed.
        darken (image): used to darken the image of an ingredient that is not owned
        lock (image): drawn above images of ingredients that are not owned
    """
    def __init__(self, path = None, x=0, y=0, rw = None, rh =None):
        self.path = path
        self.x = x
        self.y = y
        if path:
            self.image = pygame.image.load(path).convert()
            if rw:
                self.image = pygame.transform.scale(self.image, (rw,rh))
            self.darken = pygame.image.load("assets/dark.png").convert_alpha()
            self.darken.set_alpha(150)
            self.image_rect = self.image.get_rect(topleft=(x,y))
            self.darken_rect = self.darken.get_rect(topleft = (x-1,y-1))
            self.w = self.image.get_width()
            self.h = self.image.get_height()
            self.darken = pygame.transform.scale(self.darken, (self.w+2,self.h+2))
            self.lock = pygame.image.load("assets/lock.png").convert_alpha()
            self.lock_rect = self.lock.get_rect(center=(x+self.w/2,y+self.h/2))

    def draw(self, surface):
        """
        draw function draws an image of the ingredient on the screen
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        surface.blit(self.image, self.image_rect)

    def clicked(self, event):
        """
        determines whether an ingredient has been clicked down on
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
class Core(Ingredient):
    """
    A subclass from Ingredient to represent a core ingredient

    Attributes:
        spilled (int): used to see how much flour is spilled
        expected (any): determines how much of an ingredient is expected
        achieved (any): stored how much of an ingredent is achieved
    """
    def __init__(self, path, x, y,expected=None):
        super().__init__(path, x, y)
        self.spilled = 0
        if expected:
            self.expected_value = expected
        self.achieved_value = 0

class Topping(Ingredient):
    """
    A subclass from Ingredient to represent a core ingredient
    
    Attributes:
        owned (bool): stores whether the topping is owned
        added (bool): stores whether the topping has been added
        color (str): stores the color of a specific topping
        expect_rgb (list): stores the expected rgb value
        achieved_rgb (list): stores the achieved rgb value
        cost (int): the cost of the topping
        name (str): stores the name of the topping
        show_img (image): another image representation of the topping ingredient
        show_img_OG (image): used to restore the show_img when levels are reset
        slide (int): stores which page the topping will appear in the shop
        slide_pos (tuple): stores the coordinates of where the topping will appear on the shop page
        shop_img (image): the image which is shown in the shop
        buy_photo (image): button which allows a topping to be bought
        no_buy_photo (image): image which shows a topping is already owned 
    """
    def __init__(self, path, x,y, cost=None, slide = None, slide_pos = None,show_img = None,rw = None, rh =None):
        super().__init__(path, x, y, rw, rh)
        self.owned = False
        self.added = False
        self.color = ""
        self.expect_rgb = [0,0,0]
        self.achieve_rgb = [0,0,0]
        if cost != None:
            self.cost = cost
        self.name = ''
        if show_img:
            self.show_img = pygame.image.load(show_img).convert_alpha()
            self.show_img_OG = pygame.image.load(show_img).convert_alpha()
        if slide != None:
            self.slide = slide
            self.slide_pos = slide_pos
            self.shop_img = pygame.image.load(path).convert_alpha()
            self.shop_img = pygame.transform.scale(self.shop_img, (200,200))
            self.shop_img_rect = self.shop_img.get_rect(center=slide_pos)
            self.buy_photo = pygame.image.load("assets/buy.png").convert_alpha()
            self.buy_rect = self.buy_photo.get_rect(center = slide_pos)
            self.no_buy_photo = pygame.image.load("assets/no_buy.png").convert_alpha()
            self.no_buy_rect = self.no_buy_photo.get_rect(center = slide_pos)
        
    def not_owned(self,surface):
        """
        draws a message which shows a topping cannot be used as it is not owned
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        if not self.owned:
            surface.blit(self.darken,self.darken_rect)
            surface.blit(self.lock, self.lock_rect)
    
    def draw_description(self,screen,font):
        """
        draws how much each topping costs in the shop
        
        :param self: allows class attributes to be accessed
        """
        self.description = font.render(f"{self.name}: ${self.cost}", True, "Black")
        self.location = list(self.slide_pos)
        self.location[0] -= 100
        self.location[1] += 100
        screen.blit(self.description,tuple(self.location))

    def try_purchase(self,event):
        """
        checks clicking of the toppings in the shop
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.buy_rect.collidepoint(event.pos)

class level:
    """
    class for a level
    """
    def __init__(self,n):
        """
        Attributes:
        
        :param self: allows class attributes to be accessed
        :param n: the number of the level

        core_ingredients (dict): stores the core ingredients needed for that level
        add_ins (dict): stores the add ins needed for that level
        toppings (dict): stores the toppings needed for that level
        order (button): order button
        stars (int): the number of stars achieved for that level
        image (image): image of button
        x (int): x coordinate of button
        y (int): y coordinate of button
        """
        self.core_ingredients = {}
        self.add_ins = {}
        self.toppings = {}
        self.order = None
        self.stars = 5
        self.n = n
        self.image = pygame.image.load("assets/minigame.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.x = (n%8) * 125 + 312
        self.y = (n//8) * 125 + 178
        self.image_rect = self.image.get_rect(topleft = ((self.x,self.y)))
        self.Levelfont = pygame.font.Font("assets/PixelFont.otf", 20)
        if n == 0:
            self.text = self.Levelfont.render(f'Tutorial', True, (0,0,0))
        else:
            self.text = self.Levelfont.render(f'Level {n}', True, (0,0,0))
        self.text_rect = self.text.get_rect(center = (self.image_rect.w/2 +self.x, self.image_rect.h/2 +self.y))

    def draw(self, surface,number):
        """
        draws button
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        :param number: number of levels
        """
        self.score_text = self.Levelfont.render(f"{self.stars} stars", True, (0,0,0))
        surface.blit(self.image, self.image_rect)
        surface.blit(self.text, self.text_rect)
        if number>self.n+1:
            surface.blit(self.score_text, (self.x,self.y + 100))

    def clicked(self, event):
        """
        checks if button is clicked down
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
    def clickedup(self, event):
        """
        checks if button is clicked down
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONUP and self.image_rect.collidepoint(event.pos)

class egg:
    """
    a class for an egg
    """
    def __init__(self):
        """
        Attributes:
        
        :param self: allows class attributes to be accessed
        
        x (int): x coordinate of egg
        y (int): y coordinate of egg
        image (image): image of egg
        y_velocity (int): velocity the egg falls at
        collected (bool): stores whether the user collected egg with basket
        fallen (bool): stores whether the egg has fallen off screen
        """
        self.x = randint(306,1294)
        self.y = randint(-550,-75)
        self.image = pygame.image.load('assets/egg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,75))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.y_velocity = randint(2,4)
        self.collected = False
        self.fallen = False

    def draw(self, surface):
        """
        draws eggs
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        surface.blit(self.image, self.rect)

    def update(self):
        """
        updates the position of egg
        
        :param self: allows class attributes to be accessed
        """
        self.rect.y += self.y_velocity

def Home_Button(buttons, game,screen):
    """
    controls what happens where the home button is drawn depending on current screen
    
    :param buttons: dictionary of buttons
    :param game: dictionairy of boolean
    """
    if game["oven_game"]:
        buttons["home"].image_rect.x = 950
    elif game["toppings_time"]:
        buttons["home"].image_rect.x = 300
    else:
        buttons["home"].image_rect.x = 418
    buttons["home"].draw(screen)

def Home_Return(core, add, top,games,played,reset,buttons,egg_list,current):
    """
    returns the screen to home screen and resets level values
    
    :param core: dictionary of core ingredients
    :param add: dictionary of add ins
    :param top: dictionary of toppings
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param reset: dictionary of values
    :param buttons: dictionary of buttons
    :param egg_list: list of eggs
    """
    games["level_playing"] = False
    games["show_home"] = True
    games["toppings_time"] = False
    games["oven_game"] = False
    egg_list = resetting_level(core, add, top,games,played,reset,buttons,egg_list,current)
    return egg_list

def resetting_level(core, add, top,games,played,reset,buttons,egg_list,current):
    """
    resets values
    
    :param core: dictionary of core ingredients
    :param add: dictionary of add ins
    :param top: dictionary of toppings
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param reset: dictionary of values
    :param buttons: dictionary of buttons
    :param egg_list: list of eggs
    """
    for name, value in reset.items():
        reset[name][1] = reset[name][0]
    exit_clicked(games,buttons)
    for name,item in core.items():
        item.achieved_value = 0
        if name == "butter":
            item.achieved_value = []
        if name == "sugar":
            item.achieved_value = [0,0]
        item.spilled = 0
        item.added = False
    for name,item, in add.items():
        item.added = False
    for name,item, in top.items():
        item.added = False
    for name,value in played.items():
        played[name] = False
    egg_list = [egg() for i in range(5)]
    core["butter"].expected_value = copy.deepcopy(current.core_ingredients["butter"].expected_value.copy())
    sugar_salt_coordinates(reset)
    return egg_list

def exit_clicked(games,buttons):
    """
    resets values when exit button is clicked
    
    :param games: dictionary of boolean values
    :param buttons: dictionairy of buttons
    """
    for name,item in games.items():
        if name == "toppings_time" and games[name]:
            games[name] = True
        elif name == "show_home" and games[name]:
            games[name] = games[name]
        elif name == "level_playing" and games[name]:
            games[name] = games[name]
        elif name == "oven_game" and games[name]:
            games[name] = games[name]
        elif name == "oven_playing" and games[name]:
            games[name] = games[name]
        else:
            games[name] = False
    games["clicked_button"] = True
    buttons["shop_button"].clicks = 0

def homescreen(games, miniimage,leveldict,adds,tops,coins,coinstext,buttons,event,screen,font,logo,money):
    """
    changes the screen to the home screen, resets values, and controls the home screen functionality
    
    :param games: dictionary or boolean values 
    :param miniimage: image of the minigame screen
    :param leveldict: dictionary of levels
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param coins: value of money
    :param coinstext: text to display value of money
    :param buttons: dictionary of buttons
    """
    screen.fill((225, 150, 164))
    screen.blit(logo,(1600/2-265,75))
    buttons["level_button"].draw(screen)
    buttons["shop_button"].draw(screen)
    buttons["play_button"].draw(screen)
    buttons["tutorial_button"].draw(screen)

    if games["show_minigame"]:
        screen.blit(miniimage,(256,109))
        buttons["exit_button"].draw(screen)

    if games["show_levels"]:
        for name, thislevel in leveldict.items():
            thislevel.draw(screen, len(leveldict))

    if games["show_shop"]:
        coinstext = font.render(f"Balance: {money}", True, "Black")
        screen.blit(coinstext,(720,150))
        for name, add, in adds.items():
            if add.slide == buttons["shop_button"].clicks:
                screen.blit(add.shop_img,add.shop_img_rect)
                if not add.owned:
                    screen.blit(add.buy_photo,add.buy_rect)
                    add.name = name
                    add.draw_description(screen,font)
                    if add.try_purchase(event):
                        if coins>=add.cost:
                            coins -= add.cost
                            add.owned = True
                            if name in tops:
                                tops[name].owned = True
                            coinstext = font.render(f"Balance: {coins}", True, "Black")
                if add.owned:
                    screen.blit(add.no_buy_photo,add.no_buy_rect)
        for name, top, in tops.items():
            if top.slide == buttons["shop_button"].clicks and name not in adds:
                screen.blit(top.shop_img,top.shop_img_rect)
                if not top.owned:
                    screen.blit(top.buy_photo,top.buy_rect)
                    top.name = name
                    top.draw_description(screen,font)
                    if top.try_purchase(event):
                        if coins>=top.cost:
                            coins -= top.cost
                            top.owned = True
                            coinstext = font.render(f"Balance: {coins}", True, "Black")
                if top.owned:
                    screen.blit(top.no_buy_photo,top.no_buy_rect)
        if buttons["shop_button"].clicks > 0:
            buttons["next_left"].draw(screen)

        if buttons["shop_button"].clicks < 1:
            buttons["next_right"].draw(screen)
    return coins,coinstext

def addlevel(leveldict,completed,adds,tops,core_list):
    """
    creates new level and adds it to the level dictionary
    
    :param leveldict: dictionary of levels
    :param completed: dictionary of completed levels
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param core_list: dictionary of core ingredients
    """
    if completed == len(leveldict) and len(leveldict) > 0:
        leveldict[completed] = level(completed)
        Ingredients = {"order": Core(None,0,0), 
               "butter" : Core(None,342,2,[[randint(550,700),randint(400,500)],
                                           [randint(700,850),randint(400,500)],
                                            [randint(850,1050),randint(400,500)],
                                            [randint(800,1050),randint(500,600)],
                                            [randint(550,800),randint(500,600)]]),
               "eggs" : Core(None,810,0,randint(1,5)),
               "flour" : Core(None,1275,13,(randint(200,774))),
               "sugar" : Core(None,1275,320,randint(1,5)),
               "milk" : Core(None,1275,620,randint(50,230))
        }
        Adds = {"food coloring": Topping(None,0,310), 
           "chocolate chips": Topping(None,170,310), 
           "sprinkles": Topping(None,0,460), 
           "oats": Topping(None,170,460), 
           "peanuts": Topping(None,0,610), 
           "pistachios": Topping(None,170,610), 
           "matcha": Topping(None,0,760), 
           "raisins": Topping(None,170,760), 
        }

        Tops = {"icing": Topping(None,170,310), 
                "chocolate chips": Topping(None,0,510,None), 
                "sprinkles": Topping(None,0,710,None),
                "colored sugar": Topping(None,340,0), 
                "peanuts": Topping(None,547,0,None), 
                "pistachios": Topping(None,754,0,None), 
                "marshmallows": Topping(None,961,0), 
                "raisins": Topping(None,1168,0), 
                "pretzels": Topping(None,1381,0),
                "strawberries": Topping(None,1381,230), 
                "syrup": Topping(None,1381,455), 
                "coconut flakes": Topping(None,1381,685),
                }
        leveldict[completed].core_ingredients = {"eggs": Ingredients["eggs"],
                                                      "milk": Ingredients["milk"],
                                                      "flour":Ingredients["flour"],
                                                      "sugar": Ingredients["sugar"],
                                                      "butter": Ingredients["butter"]
                                                      }
        
        Colors = ["red", "green", "blue"]
        
        leveldict[completed].order = core_list["order"]
        for name, item in adds.items():
            if randint(0,2) == 1:
                if item.owned and name != "food coloring":
                    leveldict[completed].add_ins[name] = Adds[name]
                if item.owned and name == "food coloring":
                    shade = randint(0,2)
                    leveldict[completed].add_ins[name] = Adds[name]
                    leveldict[completed].add_ins[name].expect_rgb = [0,0,0]
                    leveldict[completed].add_ins[name].expect_rgb[shade] = 100
                    leveldict[completed].add_ins[name].color = Colors[shade]

        for name, item in tops.items():
            if randint(0,2) == 1:
                if item.owned and name != "icing":
                    leveldict[completed].toppings[name] = Tops[name]
                if item.owned and name == "icing":
                    chosen_color = randint(0,2)
                    leveldict[completed].toppings[name] = Tops[name]
                    leveldict[completed].toppings[name].expect_rgb = [50,50,50]
                    leveldict[completed].toppings[name].expect_rgb[chosen_color] = 255
                    leveldict[completed].toppings[name].color = Colors[chosen_color]

    return leveldict

def level_clicking(event,games,leveldict,current,buttons,core):
    """
    controls what happen when different level buttons are clicked
    
    :param event: tracks what events have occured
    :param games: dictionary of boolean values
    :param leveldict: dictionary of levels
    :param current: current level
    :param buttons: dictionary of buttons
    """
    if buttons["level_button"].is_clicked(event) and not games["show_minigame"]:
        games["show_levels"] = True
        games["show_minigame"] = True

    if buttons["play_button"].is_clicked(event) and not games["show_minigame"]:
        current = leveldict[list(leveldict)[-1]]
        games["level_playing"] = True
        games["clicked_button"] = True
    
    if buttons["tutorial_button"].is_clicked(event) and not games["show_minigame"]:
        current = leveldict["tutorial"]
        games["level_playing"] = True
        games["clicked_button"] = True

    for name, num in leveldict.items():
        if num.clicked(event) and not games["level_playing"]:
            games["clicked_button"] = True
            current = num
            games["level_playing"] = True
            games["show_minigame"] = False
        
        if num.clickedup(event):
            clicked = False
            games["show_levels"] = False
    core["butter"].expected_value = copy.deepcopy(current.core_ingredients["butter"].expected_value.copy())

    return current

def shop_clicking(games,buttons,event):
    """
    controls what happens when buttons are clicked in the shop
    
    :param games: dictionary of boolean values
    :param buttons: dictionary of buttons
    """
    if buttons["shop_button"].is_clicked(event) and not games["show_minigame"]:
        games["show_shop"] = True
        games["show_minigame"] = True

    if buttons["next_left"].is_clicked(event) and not games["clicked_button"]:
        games["clicked_button"] = True
        buttons["shop_button"].clicks -=1

    if buttons["next_right"].is_clicked(event) and not games["clicked_button"]:
        games["clicked_button"] = True
        buttons["shop_button"].clicks +=1

    if buttons["next_left"].is_clicked_up(event) or buttons["next_right"].is_clicked_up(event):
        games["clicked_button"] = False

def compare_results(current,core,adds,tops,value,games,reset,font,screen):
    """
    compares all achieved values to expected values, calculating the amount of money earned and the number of stars
    
    :param current: current level
    :param core: dictionary of core ingredients
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param value: money
    :param games: dictionary of boolean values
    :param reset: dictionary of values
    """
    wrong = set()
    if current.stars >0:
        for name,item in current.core_ingredients.items():
            if name == "butter":
                if shoelace(core[name].achieved_value) > shoelace(item.expected_value) +10 or shoelace(core[name].achieved_value) < shoelace(item.expected_value) -10:
                    wrong.add('*Incorrect value of ingredients added')
            elif name == "eggs":
                if core[name].achieved_value != item.expected_value:
                    wrong.add('*Incorrect value of ingredients added')
            elif name == "sugar":
                if core[name].achieved_value[0] != item.expected_value:
                    wrong.add('*Incorrect value of ingredients added')
                if core[name].achieved_value[1] > 0:
                    wrong.add('Salt was incorrectly added')
            elif name =="milk" or name =="flour":
                if core[name].achieved_value > item.expected_value +20 or core[name].achieved_value < item.expected_value -20:
                    wrong.add('*Incorrect value of ingredients added')
        for name,item in current.add_ins.items():
            if 'food coloring' in name:
                if adds["food coloring"].achieve_rgb != item.expect_rgb:
                    wrong.add('*Missing ingredient')
            elif not adds[name].added:
                wrong.add('*Missing ingredient')
        for add, ingredient in adds.items():
            if 'food coloring' in add:
                if 'red food coloring' not in current.add_ins and 'blue food coloring' not in current.add_ins and 'green food coloring' not in current.add_ins and ingredient.added:
                    wrong.add('*Incorrect ingredient added')
            else:
                if add not in current.add_ins and ingredient.added:
                    wrong.add('*Incorrect ingredient added')
        for name,item in current.toppings.items():
            if 'icing' in name:
                if tops["icing"].achieve_rgb != item.expect_rgb:
                    wrong.add('*Missing ingredient')
            elif not tops[name].added:
                wrong.add('*Missing ingredient')
        for top, ingredient in tops.items():
            if top not in current.toppings and ingredient.added:
                wrong.add('*Incorrect topping added')
        if reset["oven_r"][1] > 30:
            wrong.add('*Cookies baked for an incorrect period of time')
        if core["flour"].spilled >15:
            wrong.add('*Flour was spilled')
    wrong = list(wrong)
    if len(wrong) > 4:
        current.stars = 1
    else:
        current.stars = 5-len(wrong)
    price = 10
    for add,ingredient in adds.items():
        if ingredient.added:
            price += int(ingredient.cost * (current.stars*2/100))
    for top,ingredient in tops.items():
        if ingredient.added:
            price += int(ingredient.cost * (current.stars*2/100))
    price = int(price*(1+(current.stars-1)/10))
    star_text = font.render(f"{current.stars} Stars! Press next to continue!", True,(0,0,0))
    price_text = font.render(f"You've earned ${price}", True, (0,0,0))
    lost_text = font.render(f"You've lost stars because:", True, (0,0,0))
    screen.blit(star_text,(400,200))
    screen.blit(price_text,(400,250))
    if len(wrong)>0:
        screen.blit(lost_text,(400,350))
        for i in range(len(wrong)):
            text = font.render(wrong[i], True, (0,0,0))
            screen.blit(text,(400,400+50*i))
    if not games["added_price"]:
        value += price
        games["added_price"] = True
    return value
