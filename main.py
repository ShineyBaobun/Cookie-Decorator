import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("assets/PixelFont.otf", 20)
Money = 0

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
    
    def draw_description(self):
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

class Button:
    """
    A class for a button
    """
    def __init__(self,w=100,h=100,x=100,y=100,image=None, name = None):
        """
        Attributes:
        
        :param self: allows class attributes to be accessed
        :param w: button width
        :param h: button height
        :param x: button x coordinate
        :param y: button y coordinate
        :param image: the image of the button
        :param name: the name of the button

            text: text of name of button
            clicks: tracks how many times a button has been clicked
        """
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.image_rect = self.image.get_rect(center = (x,y))
        self.text = None
        self.clicks = 0
        if name:
            self.text = font.render(f'{name}', True, (0,0,0))
            self.text_rect = self.text.get_rect(center=(x,y))
    
    def draw(self, surface):
        """
        draw function draws the button on the screen
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        """
        surface.blit(self.image, self.image_rect)
        if self.text:
            surface.blit(self.text, self.text_rect)

    def is_clicked_up(self, event):
        """
        tracks whether buttos is clicked up
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONUP and self.image_rect.collidepoint(event.pos)
    
    def is_clicked(self,event):
        """
        tracks whether buttos is clicked down
        
        :param self: allows class attributes to be accessed
        :param event: tracks what events have occured
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
  
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
        if n == 0:
            self.text = font.render(f'Tutorial', True, (0,0,0))
        else:
            self.text = font.render(f'Level {n}', True, (0,0,0))
        self.text_rect = self.text.get_rect(center = (self.image_rect.w/2 +self.x, self.image_rect.h/2 +self.y))

    def draw(self, surface,number):
        """
        draws button
        
        :param self: allows class attributes to be accessed
        :param surface: determines where the image will be drawn
        :param number: number of levels
        """
        self.score_text = font.render(f"{self.stars} stars", True, (0,0,0))
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
        self.x = randint(minigame_rect.x + 50,minigame_rect.x + minigame.get_width()-50)
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
        self.rect.y += 3

def HomeButton(buttons, game):
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

def HomeReturn(core, add, top,games,played,reset,buttons,egg_list):
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
    egg_list = resetting_level(core, add, top,games,played,reset,buttons,egg_list)
    return egg_list

def resetting_level(core, add, top,games,played,reset,buttons,egg_list):
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
    exitclicked(games,buttons)
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
    sugar_salt_coordinates(reset)
    return egg_list

def exitclicked(games,buttons):
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

def tutorial_instructions(x,y,message,angle):
    """
    creates a new instance of an arrow and a message used for the tutorial level
    
    :param x: x coordinate
    :param y: y coordinate
    :param message: the message to be drawn
    :param angle: angle of the arrow drawn
    """
    text = font.render(message,True,(0,0,0),(255,255,255))
    arrow = pygame.image.load("assets/tutorial_arrow.png").convert_alpha()
    arrow = pygame.transform.rotate(arrow, angle)
    arrow_rect = arrow.get_rect(topleft = (x,y))
    screen.blit(arrow,arrow_rect)
    screen.blit(text,(x+225,y+100))

def tutorial_process(games,played,adds,tops):
    """
    draws instructions for the tutorial level
    
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    """
    if not games["toppings_time"] and not games["oven_game"]:
        if not any(played.values()) and not games["show_minigame"]:
            tutorial_instructions(280,200,"View order to see what ingredients to add",0)
        if not played["butter_played"] and games["order_open"]:
            tutorial_instructions(500,70,"Remember how much butter to add",32)
            played["order_opened"] = True
        if not played["butter_played"] and not games["show_minigame"] and played["order_opened"]:
            tutorial_instructions(400,200,"Click to add butter",-45)
        if games["butter_game"] and not played["butter_played"]:
            tutorial_instructions(720,200,"Click all 5 verticies to cut butter",100)
        if played["butter_played"] and not games["show_minigame"] and not played["eggs_played"]:
            tutorial_instructions(300,200,"Great job! Continue to check the order to see what other ingredients to add",0)
        if games["eggs_game"] and not played["eggs_played"]:
            tutorial_instructions(720,600,"Press the left and right keys to control your basket",-58)
        if games["sugar_game"] and not played["sugar_played"]:
            tutorial_instructions(600,600,"Press the left and right keys to control your basket. Avoid the salt!",-58)
        if games["flour_game"] and not played["flour_played"]:
            tutorial_instructions(600,600,"Press the down key to pour flour. Be careful to not let any spill!",-58)
        if games["milk_game"] and not played["milk_played"]:
            tutorial_instructions(600,250,"Press once to start pouring and once to stop. You only have one chance!",-98)
        if games["add_coloring"]:
            tutorial_instructions(280,100,"Don't add food coloring! It's not in the order. Press X to close.",0)
        if played["butter_played"] and played["eggs_played"] and played["sugar_played"] and played["flour_played"] and played["milk_played"] and not adds["chocolate chips"].added and not games["show_minigame"]:
            tutorial_instructions(310,300,"Don't forget to add chocolate chips!",32)
        if played["butter_played"] and played["eggs_played"] and played["sugar_played"] and played["flour_played"] and played["milk_played"] and adds["chocolate chips"].added and not games["show_minigame"]:
            tutorial_instructions(800,600,"Press next to continue",-180)
    if not games["toppings_time"] and games["oven_game"]:
        if not games["oven_playing"] and not played["oven_played"]:
            tutorial_instructions(900,150,"Press start to start baking your cookies",122)
        if games["oven_playing"]:
            tutorial_instructions(720,10,"When the bar reaches the end click stop",32)
        if played["oven_played"]:
            tutorial_instructions(970,580,"Press next to continue",122)
    if games["toppings_time"] and not games["oven_game"]:
        if games["order_open"]:
            played["order_opened"] = True
        if not played["order_opened"] and not games["show_minigame"]:
            tutorial_instructions(280,200,"View order to see what toppings to add",0)
        if played["order_opened"] and not games["added_icing"] and not games["show_minigame"]:
            tutorial_instructions(0,450,"Add food coloring",-58)
        if games["add_icing"] and games["show_minigame"]:
            tutorial_instructions(470,520,"Add red food coloring",-58)

def homescreen(games, miniimage, minirect,leveldict,adds,tops,coins,coinstext,buttons):
    """
    changes the screen to the home screen, resets values, and controls the home screen functionality
    
    :param games: dictionary or boolean values 
    :param miniimage: image of the minigame screen
    :param minirect: rect for the image of the minigame screen
    :param leveldict: dictionary of levels
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param coins: value of money
    :param coinstext: text to display value of money
    :param buttons: dictionary of buttons
    """
    screen.fill((225, 150, 164))
    buttons["level_button"].draw(screen)
    buttons["shop_button"].draw(screen)
    buttons["play_button"].draw(screen)
    buttons["tutorial_button"].draw(screen)

    if games["show_minigame"]:
        screen.blit(miniimage,minirect)
        buttons["exit_button"].draw(screen)

    if games["show_levels"]:
        for name, thislevel in leveldict.items():
            thislevel.draw(screen, len(leveldict))

    if games["show_shop"]:
        coinstext = font.render(f"Balance: {Money}", True, "Black")
        screen.blit(coinstext,(720,150))
        for name, add, in adds.items():
            if add.slide == buttons["shop_button"].clicks:
                screen.blit(add.shop_img,add.shop_img_rect)
                if not add.owned:
                    screen.blit(add.buy_photo,add.buy_rect)
                    add.name = name
                    add.draw_description()
                    if add.try_purchase(event):
                        if coins>=add.cost:
                            coins -= add.cost
                            add.owned = True
                            coinstext = font.render(f"Balance: {coins}", True, "Black")
                if add.owned:
                    screen.blit(add.no_buy_photo,add.no_buy_rect)
        for name, top, in tops.items():
            if top.slide == buttons["shop_button"].clicks and name not in adds:
                screen.blit(top.shop_img,top.shop_img_rect)
                if not top.owned:
                    screen.blit(top.buy_photo,top.buy_rect)
                    top.name = name
                    top.draw_description()
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
    if len(completed) <= len(leveldict) and len(leveldict) > 0:
        leveldict[len(completed)] = level(len(completed))
        Ingredients = {"order": Core(None,0,0), 
               "butter" : Core(None,342,2,[[randint(550,700),randint(400,500)],
                                           [randint(700,850),randint(400,500)],
                                            [randint(850,1050),randint(400,500)],
                                            [randint(800,1050),randint(500,600)],
                                            [randint(550,800),randint(500,600)]]),
               "eggs" : Core(None,810,0,randint(1,5)),
               "flour" : Core(None,1275,13,(randint(200,774))),
               "sugar" : Core(None,1275,320,randint(1,5)),
               "milk" : Core(None,1275,620,randint(100,560))
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

        Tops = {"icing": Topping(None,0,310), 
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
        leveldict[len(completed)].core_ingredients = {"eggs": Ingredients["eggs"],
                                                      "milk": Ingredients["milk"],
                                                      "flour":Ingredients["flour"],
                                                      "sugar": Ingredients["sugar"],
                                                      "butter": Ingredients["butter"]
                                                      }
        
        Colors = ["red", "green", "blue"]
        
        leveldict[len(completed)].order = core_list["order"]
        for name, item in adds.items():
            if randint(0,2) == 1:
                if item.owned and name != "food coloring":
                    leveldict[len(completed)].add_ins[name] = Adds[name]
                if item.owned and name == "food coloring":
                    shade = randint(0,2)
                    leveldict[len(completed)].add_ins[f"{Colors[shade]} food coloring"] = Adds[name]
                    leveldict[len(completed)].add_ins[f"{Colors[shade]} food coloring"].expect_rgb[shade] += 100

        for name, item in tops.items():
            if randint(0,2) == 1:
                if item.owned and name != "icing":
                    leveldict[len(completed)].toppings[name] = Tops[name]
                if item.owned and name == "icing":
                    chosen_color = randint(0,2)
                    leveldict[len(completed)].toppings[name] = Tops[name]
                    leveldict[len(completed)].toppings[name].expect_rgb = [50,50,50]
                    leveldict[len(completed)].toppings[name].expect_rgb[chosen_color] = 255
                    leveldict[len(completed)].toppings[name].color = Colors[chosen_color]

    return leveldict

def level_clicking(event,games,leveldict,current,buttons):
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

    return current

def shop_clicking(games,buttons):
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

def addclicking(adds, games,reset):
    """
    controls what happens when different add ins are clicked and added to the cookies
    
    :param adds: dictionary of add ins
    :param games: dictionary of boolean values
    :param reset: dictionary of values
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
                    if name == "pistachio":
                        reset["bowl_color"][1] = (147, 197, 114)
                    if name == "matcha":
                        reset["bowl_color"][1] = (145, 181, 0)
                    if name == "raisins":
                        reset["bowl_color"][1] = (36, 33, 36)
                if name == "food coloring":
                    games["add_coloring"] = True
            if not item.owned and not games["toppings_time"]:
                games["not_owned_mini"] = True

def topclicking(tops,games):
    """
    controls what happens when different toppings are clicked and added to the cookies
    
    :param tops: dictionary of toppings
    :param games: dictionary of boolean values
    """
    for name, item in tops.items():
        if item.clicked(event): 
            if item.owned:
                if name == "icing":
                    games["add_icing"] = True
                    games["show_minigame"] = True
                else:
                    item.added = True
            if not item.owned:
                games["not_owned_mini"] = True
    return

def add_top_draw(adds,tops,games):
    """
    draws different images based on which add ins and toppings were added to the cookes
    
    :param adds: dictionary of add ins
    :param tops: dictionary of toppings
    :param games: dictionary of boolean values
    """
    if games["added_icing"]:
        tops["icing"].added = True
        games["add_icing"] = False
    if not games["show_minigame"]:
        for name, item in adds.items():
            if name == "matcha" and item.added:
                g+=50
            if name != "food coloring" and name!= "matcha" and item.added and games["toppings_time"]:
                screen.blit(item.show_img, (0,0))
        for name, item in tops.items():
            if item.added:
                screen.blit(item.show_img, (0,0))
            if games["not_owned_mini"]:
                games["show_minigame"] = True

def choosecolor(colors,games,adds,reset):
    """
    stores which color of food coloring was added
    
    :param colors: dictionary of color buttons
    :param games: dictionary of boolean values
    :param adds: dictionary of add ins
    :param reset: dictionary of values
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

def chooseicing(colors,games,tops):
    """
    stores which color of icing was added to cookies
    
    :param colors: dictionary of color buttons
    :param games: dictionary of boolean values
    :param tops: dictionary of toppings
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

def compare_results(current,core,adds,tops,value,games,reset):
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
            else:
                if core[name].achieved_value > item.expected_value +20 or core[name].achieved_value < item.expected_value -20:
                    wrong.add('*Incorrect value of ingredients added')
        for name,item in current.add_ins.items():
            if 'food coloring' in name:
                if adds["food coloring"].achieve_rgb != item.expect_rgb:
                    wrong.add('*Missing ingredient')
            elif not adds[name].added:
                wrong.add('*Missing ingredient')
        for add, ingredient in adds.items():
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
    star_text = font.render(f"{current.stars} Stars! Press next to continue!", True,(0,0,0))
    price_text = font.render(f"You've earned ${price}", True, (0,0,0))
    lost_text = font.render(f"You've lost stars because:", True, (0,0,0))
    screen.blit(star_text,(400,300))
    screen.blit(price_text,(400,350))
    if len(wrong)>0:
        screen.blit(lost_text,(400,400))
        for i in range(len(wrong)):
            text = font.render(wrong[i], True, (0,0,0))
            screen.blit(text,(400,450+50*i))
    if not games["added_price"]:
        value += price
        games["added_price"] = True
    return value

def egg_collisions(egg_list,left,right,bottom,top,length,core,games,played,text,reset):
    """
    tracks if eggs collide with basket and controls how eggs move within the basket and outside it
    
    :param egg_list: list od eggs
    :param left: left side of basket
    :param right: right side of basket
    :param bottom: bottom of basket
    :param top: top of basket
    :param length: height of screen
    :param core: dictionary of core ingredients
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param text: text that displays number of eggs collected
    :param reset: dictionary of values
    """
    for egg in egg_list:
        egg.update() 
        if egg.rect.colliderect(left) and egg.rect.x > left.x:
            egg.rect.x = left.x + 10
        if egg.rect.colliderect(left) and egg.rect.x <= left.x:
            egg.rect.x = left.x-50
        if egg.rect.colliderect(right) and egg.rect.x < right.x:
            egg.rect.x = right.x -50
        if egg.rect.colliderect(right) and egg.rect.x > right.x:
            egg.rect.x = right.x + 11
        if egg.rect.colliderect(bottom):        
            egg.rect.y = bottom.y -75
        if egg.rect.colliderect(top) and not egg.collected:        
            core["eggs"].achieved_value += 1
            text = font.render(f"Eggs: {core["eggs"].achieved_value}", True, (0,0,0))
            egg.collected = True
            reset["egg_fallen"][1] += 1
        if egg.rect.top >= length and not egg.fallen:
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

def basket_update(rect,bottom,left,right,top):
    """
    updates the position of the basket
    
    :param rect: the rect of basket as a whole
    :param bottom: rect of the bottom of the basket
    :param left: rect of the left side of the basket
    :param right: rect of the right side of the basket
    :param top: rect of the top of the basket
    """
    bottom.update(rect.x, rect.y+rect.height-10, rect.width, 10)
    left.update(rect.x, rect.y, 10, rect.height)
    right.update(rect.x+rect.width-10, rect.y, 10, rect.height)
    top.update(rect.x+10, rect.y, rect.width-20, 10)
    
def eggcontrols(basket,basketrect,minirect,bottom,left,right,top,egglist):
    """
    controls what happens when keys are pressed in the egg game
    
    :param basket: the image of the basket
    :param basketrect: the rect of the basket
    :param minirect: the rect of the mini game background
    :param bottom: the rect of the bottom of the basket
    :param left: left rect of backet
    :param right: right rect of basket
    :param top: top rect of basket
    :param egglist: list of eggs
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basketrect.x > minirect.x:
        basketrect.x -= 9
    if keys[pygame.K_RIGHT] and basketrect.x < 800+minirect.width/2 - basketrect.width:
        basket_rect.x += 9
    basket_update(basketrect, bottom, left,right,top)

    screen.blit(basket, basketrect)

    for egg in egglist:
        egg.draw(screen)

def milkclicking(can):
    """
    controls what happens during clicking in the milk game
    
    :param can: the milk can (object of bottle class)
    """
    if can.clicked(event):
        can.toggle_rotation()
        if not can.poured and can.turned:
            can.poured = True

def milk_game_controls(can,core,games,played,text,reset):
    """
    controls what is drawn during the milk game
    
    :param can: object from the bottle class
    :param core: dictionary of core ingredients
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param text: text that displays the volume of milk collected
    :param reset: dictionary of values
    """
    can.draw(screen)
    milk_cup = pygame.draw.rect(screen, "black", [700, 400, 300, 300], 10)
    milk_fill = pygame.draw.rect(screen, "white", [710, reset["milk_y"][1], 280, reset["milk_h"][1]])
    
    if can.turned:
        milk_liquid = pygame.draw.rect(screen, "white", [840,213,10,477])
        reset["milk_h"][1]+=1
        reset["milk_y"][1]-=1
        core["milk"].achieved_value += 2
        text = font.render(f"Volume: {core["milk"].achieved_value}", True, "Black")

    if can.turned and core["milk"].achieved_value >= 560:
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

def flourfalling(right,pour,core,image,imagerect,complete,completerect,flour_volume_text,reset):
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
    """
    screen.blit(image,imagerect)
    cup = pygame.draw.imagerect(screen, "black", [reset["sieve_x"][1], 400, 300, 300], 10)
    fill = pygame.draw.imagerect(screen, "white", [reset["sieve_x"][1]+10, reset["sieve_y"][1], 280, reset["sieve_h"][1]])
    screen.blit(complete,completerect)
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
        flourfront = pygame.draw.imagerect(screen, "white", [reset["flour_front_x"][1],imagerect.y + 150,reset["flour_front_w"][1],800])
        flourback = pygame.draw.imagerect(screen, "white", [imagerect.x + 75,imagerect.y + 150,150, cup.y - imagerect.y + 140])
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

def flourkeys(games,pour,played,reset):
    """
    controls what happens when keys are pressed during the flour game
    
    :param games: dictionary of boolean values
    :param pour: boolean value which shows whether flour is being poured
    :param played: dictionary of boolean vlaues
    :param reset: dictionary of values
    """
    flour_keys = pygame.key.get_pressed()
    if flour_keys[pygame.K_DOWN]:
        pour = True
    else: 
        pour = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if flour_complete_rect.collidepoint(mouse_pos):
            reset["bowl_color"][1] = (245, 236, 226)
            reset["bowl_r"][1]+= 10
            games["flour_game"] = False
            played["flour_played"] = True
            games["show_minigame"] = False
    return pour

def sugarkeys(rect,container,bottom,left,right,top):
    """
    controls what happens when keys are pressed during the sugar game
    
    :param rect: rect of the basket
    :param container: image of basket
    :param bottom: bottom rect of basket
    :param left: left rect of basket
    :param right: right rect of basket
    :param top: top rect of basket
    """
    sugar_keys = pygame.key.get_pressed()
    if sugar_keys[pygame.K_LEFT] and rect.x != width/2-(container.get_width()/2)-400:
        rect.x -= 400
    if sugar_keys[pygame.K_RIGHT] and rect.x != width/2-(container.get_width()/2)+400:
        rect.x += 400
    basket_update(rect, bottom, left,right,top)

def sugar_salt_coordinates(reset):
    """
    calculates the coordinates/column of each row of sugar and salt
    
    :param reset: dictionary of values
    """
    for i in range(5):
        nums = [375,width/2-37,1150]
        chosen_x = nums[randint(0,2)]
        reset["SugarSalts"][1].append(SugarSalt(-50-(i*200),"sugar",chosen_x))
        nums.remove(chosen_x)
        chosen_x = nums[randint(0,1)]
        reset["SugarSalts"][1].append(SugarSalt(-50-(i*200),"salt", chosen_x))

def sugarcontrols(top,left,right,games,played,core,sugarstext,saltstext,reset):
    """
    controls what happens during collisions and what is drawn during the sugar game
    
    :param top: top rect of basket
    :param left: left rect of basket
    :param right: right rect of basket
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param core: dictionary of core ingredients
    :param sugarstext: text that displays how many sugars have been collected
    :param saltstext: text that displays how many salts have been collected
    :param reset: dictionary of values
    """
    for ingredient in reset["SugarSalts"][1]:
        ingredient.update()
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "sugar":        
            core["sugar"].achieved_value[0] += 1
            reset["SugarSalts"][1].remove(ingredient)
            sugarstext = font.render(f"Sugar Collected: {core["sugar"].achieved_value[0]}", True, "Black")
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "salt":        
            reset["SugarSalts"][1].remove(ingredient)
            core["sugar"].achieved_value[1] += 1
            saltstext = font.render(f"Salt Collected: {core["sugar"].achieved_value[1]}", True, "Black")
        if ingredient.rect.y >= 900:
            reset["SugarSalts"][1].remove(ingredient)

    for ingredient in reset["SugarSalts"][1]:
        ingredient.draw(screen)
    screen.blit(basket, basket_rect)

    screen.blit(sugarstext,(950,150))
    screen.blit(saltstext,(950,200))

    if not reset["SugarSalts"][1]:
        reset["bowl_color"][1] = (255, 255, 255)
        reset["bowl_r"][1] += 10
        games["sugar_game"] = False
        played["sugar_played"] = True
        games["show_minigame"] = False

    return sugarstext,saltstext

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

def butterclicking(core,back,games,text):
    """
    controls what happens during clicking in the butter game
    
    :param core: dictionary of core ingredients
    :param back: rect of the back of butter
    :param games: dictionary of boolean values
    :param text: text that displays the volume of butter cut
    """
    if len(core["butter"].achieved_value)<=4:
        mouse_pos = event.pos
        if back.collidepoint(mouse_pos) and not games["clicked_button"]:
            core["butter"].achieved_value.append(pygame.mouse.get_pos())

    text = font.render(f"Current volume: {int(shoelace(core["butter"].achieved_value)/1000)}", True, "black")
    return text

def butterdrawing(current,games,played,fallen,text,core,reset):
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
        pygame.draw.line(screen, "green", (current.core_ingredients["butter"].expected_value[i%5][0],current.core_ingredients["butter"].expected_value[i%5][1]),(current.core_ingredients["butter"].expected_value[(i+1)%5][0],current.core_ingredients["butter"].expected_value[(i+1)%5][1]),10)
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
            current.core_ingredients["butter"].expected_value[i][1] += 5
        reset["butter_back_y"][1] += 5

    if butter_back.y >= 900:
        games["butter_game"] = False
        played["butter_played"] = True
        games["show_minigame"] = False

    screen.blit(text,(950,150))
    
    return fallen

def order_recipe(texts, current, games, buttons):
    """
    draws order when the order is open
    
    :param texts: dictionary of texts to be displayed
    :param current: current level
    :param games: dictionary of boolean values
    :param buttons: dictionary of buttons
    """
    games["show_minigame"] = True
    buttons["exit_button"].draw(screen)
    if not games["toppings_time"]:
        texts["core"] = font.render(f"Core Ingredients:", True, "Black")
        screen.blit(texts["core"],(400,150))
        for i, (name, expected) in enumerate(current.core_ingredients.items()):
            if name == "butter":
                value = int(shoelace(expected.expected_value)/1000)
            else:
                value = expected.expected_value
            texts[name] = font.render(f"{name}:{value}", True, "Black")
            screen.blit(texts[name],(400,150+(1+i)*40))
        for i, (name, expected) in enumerate(current.add_ins.items()):
            texts[name] = font.render(f"{name}", True, "Black")
            screen.blit(texts[name],(400,350+(1+i)*40))
    if  games["toppings_time"]:
        texts["top"] = font.render(f"Toppings:", True, "Black")
        screen.blit(texts["top"],(400,150))
        for i, (name, expected) in enumerate(current.toppings.items()):
            if name == "icing":
                texts[name] = font.render(f"{item.color} {name}", True, "Black")
            else:
                texts[name] = font.render(f"{name}", True, "Black")
            screen.blit(texts[name],(400,150+(i+1)*40))
    return texts

def ovendraw(image,image_rect,reset,games,buttons):
    """
    controls what is drawn during the oven game
    
    :param image: image of oven
    :param image_rect: rect of oven
    :param reset: dictionary of values
    :param games: dictionary of boolean values
    :param buttons: dictionary of buttons
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

def ovenclicking(games,played,buttons):
    """
    controls what happens during clicking in the oven game
    
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param buttons: dictionary of buttons
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

def nextclicking(games, played, current,level_list,completed_list,add,top,core,reset,buttons,egg_list):
    """
    determines what happens when the next button is clicked on different screens
    
    :param games: dictionary of boolean values
    :param played: dictionary of boolean values
    :param current: current level
    :param level_list: dictionary of level
    :param completed_list: dictionary of completed levels
    :param add: dictionary of add ins
    :param top: dictionary of toppings
    :param core: dictionary of core ingredients
    :param reset: dictionary of values
    :param buttons: dictionary of buttons
    :param egg_list: list of eggs
    """
    if buttons["next"].is_clicked(event) and not games["clicked_button"]and not games["show_shop"]:
        games["clicked_button"] = True
        if not played["oven_played"]:
                games["oven_game"] = True
                games["startbutton_show"] = True
        elif played["oven_played"] and not games["toppings_time"]:
            games["toppings_time"] = True
            games["oven_game"] = False
            played["order_opened"] = False
        elif games["toppings_time"]:
            if not games["finished_screen"]:
                games["finished_screen"] = True
                return current,level_list,egg_list
            completed_list[len(completed_list)] = current
            level_list = addlevel(level_list,completed_list,add,top,Core_Ingredient)
            current = level_list[len(completed_list)]
            games["toppings_time"] = False
            egg_list = resetting_level(core, add, top,games,played,reset,buttons,egg_list)
            return current,level_list,egg_list

    if buttons["next"].is_clicked_up(event):
        games["clicked_button"] = False

    return current,level_list,egg_list

background = pygame.image.load("assets/Kitchen.png").convert()
minigame = pygame.image.load("assets/minigame.png").convert_alpha()
minigame_rect = minigame.get_rect(topleft=((1600/2)-minigame.get_width()/2,(900/2)-minigame.get_height()/2))
traybackground = pygame.image.load("assets/traybackground.png").convert_alpha()
already_played_text = font.render("Ingredient already added", True, (0,0,0))
balance_text = font.render(f"Balance: {Money}", True, "Black")
tutorial_arrow = pygame.image.load("assets/tutorial_arrow.png").convert_alpha

completed_levels = {}
levels = {"tutorial": level(0)
          }

Core_Ingredient = {"order": Core("assets/order.png",0,0), 
               "butter" : Core("assets/buttertray.png",342,2,[[550,500],[800,400], [1050,500], [925,600], [675,600]]),
               "eggs" : Core("assets/eggtray.png",810,0,2),
               "flour" : Core("assets/flour.png",1275,13,500),
               "sugar" : Core("assets/sugar.png",1275,320,300),
               "milk" : Core("assets/milk.png",1275,620,200)
        }

Add_Ins = {"food coloring": Topping("assets/coloring.png",0,310,0,0,(425,300)), 
           "chocolate chips": Topping("assets/chocchips.jpg",170,310,0,0,(675,300),"assets/ChocChipAdd.PNG"), 
           "sprinkles": Topping("assets/sprinkles.jpg",0,460,100,0,(925,300),"assets/SprinkleAdd.PNG"), 
           "oats": Topping("assets/oats.jpg",170,460,100,0,(1175,300),"assets/OatsAdd.PNG"), 
           "peanuts": Topping("assets/peanuts.jpg",0,610,150,1,(425,300),"assets/PeanutAdd.PNG"), 
           "pistachios": Topping("assets/pistachios.jpg",170,610,150,1,(675,300),"assets/PistachioAdd.PNG"), 
           "matcha": Topping("assets/matcha.jpg",0,760,300,1,(925,300)), 
           "raisins": Topping("assets/raisins.jpg",170,760,300,1,(1175,300),"assets/RaisinsAdd.PNG"), 
        }

Toppings = {"icing": Topping("assets/icing.jpg",0,310,0,0,(425,600),"assets/IcingTop.PNG"), 
           "chocolate chips": Topping("assets/chocchips.jpg",0,510,0,0,(0,600),"assets/ChocChipTop.PNG",210,180), 
           "sprinkles": Topping("assets/sprinkles.jpg",0,710,150,0,(0,600),"assets/SprinkleTop.PNG",210,180),
           "colored sugar": Topping("assets/coloredsugar.jpg",340,0,150,0,(675,600),"assets/ColoredSugarTop.PNG"), 
           "peanuts": Topping("assets/peanuts.jpg",547,0,150,1,(0,600),"assets/PeanutTop.PNG",190,202), 
           "pistachios": Topping("assets/pistachios.jpg",754,0,150,1,(0,600),"assets/PistachioTop.PNG",190,202), 
           "marshmallows": Topping("assets/marshmallows.jpg",961,0,300,0,(925,600),"assets/MarshmallowTop.PNG"), 
           "raisins": Topping("assets/raisins.jpg",1168,0,300,1,(1175,600),"assets/RaisinsTop.PNG",190,202,), 
           "pretzels": Topping("assets/pretzels.jpg",1381,0,400,0,(1175,600),"assets/PretzelsTop.PNG"),
           "strawberries": Topping("assets/strawberries.jpg",1381,230,500,1,(425,600),"assets/StrawberriesTop.PNG"), 
           "syrup": Topping("assets/syrup.jpg",1381,455,500,1,(675,600),"assets/SyrupTop.PNG"), 
           "coconut flakes": Topping("assets/coconut.webp",1381,685,600,1,(925,600),"assets/CoconutTop.PNG"),
        }

Add_Ins["food coloring"].owned = True
Add_Ins["chocolate chips"].owned = True
Toppings["icing"].owned = True
Toppings["chocolate chips"].owned = True

levels["tutorial"].core_ingredients = {"butter" : Core("assets/buttertray.png",342,2,[[550,500],[800,400], [1050,500], [925,600], [675,600]]),
               "eggs" : Core("assets/eggtray.png",810,0,2),
               "flour" : Core("assets/flour.png",1275,13,500),
               "sugar" : Core("assets/sugar.png",1275,320,3),
               "milk" : Core("assets/milk.png",1275,620,200)}

levels["tutorial"].order = Core("assets/order.png",0,0)
levels["tutorial"].add_ins = {'chocolate chips': Add_Ins["chocolate chips"]}
levels["tutorial"].toppings = {"icing": Toppings['icing'],
                               "chocolate chips": Toppings['chocolate chips']}

levels["tutorial"].toppings["icing"].expect_rgb = [255,50,50]
levels["tutorial"].color = "red"

current_level = levels["tutorial"]

Buttons = {"level_button": Button(400,100,width/2,height/2 - 50,'assets/minigame.png', "Levels"),
           "shop_button": Button(400,100,width/2,height/2 +75,'assets/minigame.png',"Shop"),
           "play_button": Button(400,100,width/2,height/2 +200,'assets/minigame.png',"Play"),
           "tutorial_button": Button(400,100,width/2,height/2 +325,'assets/minigame.png',"Tutorial"),
           "exit_button": Button(55,55,minigame_rect.x+27, minigame_rect.y+28,'assets/exit.png'),
           "home": Button(86,83,418,841,"assets/home.png"),
           "next": Button(142,93,1146,846,"assets/nextbutton.png"),
           "next_right": Button(142,93,1300,450,"assets/next_right.png"),
           "next_left": Button(142,93,300,450,"assets/next_left.png"),
           "buy_button": Button(75,50,800,450,"assets/next_left.png"),
           "startbutton": Button(523,178,1200,450,"assets/startbutton.png"),
           "stopbutton": Button(523,178,1200,450,"assets/stopbutton.png")}

Color_Buttons = {
    "red": Button(100,100,600,500,"assets/red.png","Red"),
    "green": Button(100,100,800,500,"assets/green.png","Green"),
    "blue": Button(100,100,1000,500,"assets/blue.png","Blue"),
}

not_owned_text = font.render("Ingredient Not Owned. Buy in Shop", True, (0,0,0))

basket = pygame.image.load('assets/basket.png').convert_alpha()
basket = pygame.transform.scale(basket, (250,150))
basket_rect = basket.get_rect()
basket_rect.topleft = (width/2-(basket.get_width()/2),500)
basket_bottom = pygame.Rect(basket_rect.x,
                    basket_rect.y+basket_rect.height-10,
                    basket_rect.width,
                    10)
basket_left = pygame.Rect(basket_rect.x,
                    basket_rect.y,
                    10,
                    basket_rect.height)
basket_right = pygame.Rect(basket_rect.x+basket_rect.width-10,
                    basket_rect.y,
                    10,
                    basket_rect.height)
basket_top = pygame.Rect(basket_rect.x+10, 
                            basket_rect.y, 
                            basket_rect.width-20, 
                            10)

eggs = [egg() for i in range(5)]
egg_text = font.render(f"Eggs: {Core_Ingredient["eggs"].achieved_value}", True, (0,0,0))

milk_can = Bottle(930, 230, 100,150)
milk_text = font.render(f"Volume: {Core_Ingredient["milk"].achieved_value}", True, "Black")

sieve = pygame.image.load("assets/sieve.png").convert_alpha()
sieve = pygame.transform.scale(sieve, (250,150))
sieve_rect = sieve.get_rect(center=(width/2,height/2-200))
flour_right = True
flour_pour = False
flour_complete = pygame.image.load("assets/checkbox.png").convert()
flour_complete = pygame.transform.scale(flour_complete, (100,100))
flour_complete_rect = flour_complete.get_rect(center = (width/2+350,height/2-150))
flour_text = font.render(f"Volume: {int(Core_Ingredient["flour"].achieved_value/100)}", True, "Black")

reset_constants = {"bowl_color": [None, None],
                   "bowl_r": [150,150],
                   "egg_fallen": [0,0],
                   "milk_h": [0,0],
                   "milk_y": [690,690],
                   "sieve_y": [690,690],
                   "sieve_x": [600,600],
                   "sieve_h": [0,0],
                   "flour_front_w": [150,150],
                   "flour_front_x": [sieve_rect.x + 75,sieve_rect.x + 75],
                   "SugarSalts": [[],[]],
                   "butter_back_y": [height/2-50,height/2-50],
                   "oven_width": [0,0],
                   "oven_r": [255,255],
                   "oven_g": [255,255],
                   "oven_b": [255,255],
                   "cookies": [pygame.image.load("assets/Cookies.PNG").convert_alpha(),pygame.image.load("assets/Cookies.PNG").convert_alpha()]}

basket_rect.topleft = (width/2-(basket.get_width()/2),500)

sugar_salt_coordinates(reset_constants)
Core_Ingredient["sugar"].achieved_value = [0,0]
sugar_text = font.render(f"Sugar Collected: {Core_Ingredient["sugar"].achieved_value[0]}", True, "Black")
salt_text = font.render(f"Salt Collected: {Core_Ingredient["sugar"].achieved_value[1]}", True, "Black")

Core_Ingredient["butter"].achieved_value = []
fallen_butter = []

butter_expected_total = shoelace(current_level.core_ingredients["butter"].expected_value)
butter_back = pygame.Rect([width/2-250,reset_constants["butter_back_y"][1],500,200,])
butter_text = font.render(f"Current volume: 0", True, "black")

order_texts = {}

oven = pygame.image.load("assets/oven.png").convert_alpha()
oven_rect = oven.get_rect(center = (500,450))

Games = {"eggs_game": False,
         "milk_game": False,
         "flour_game": False,
         "sugar_game": False,
         "butter_game": False,
         "show_minigame": False,
         "oven_game": False,
         "show_levels": False,
         "clicked_button": False,
         "order_open": False,
         "already_played": False,
         "show_colors": False,
         "finished_screen": False,
         "toppings_time": False,
         "add_coloring": False,
         "add_icing": False,
         "added_icing": False,
         "show_shop": False,
         "added_price": False,
         "show_home": True,
         "level_playing": False,
         "oven_playing": False,
         "startbutton_show": False,
         "not_owned_mini": False,
         }

Played = {"eggs_played": False,
          "milk_played": False,
          "flour_played": False,
          "sugar_played": False,
          "butter_played": False,
          "oven_played": False,
          "order_opened": False}

running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if Games["show_home"] and not Games["level_playing"]:
            current_level = level_clicking(event,Games,levels,current_level,Buttons)
            shop_clicking(Games,Buttons)

        if Buttons["exit_button"].is_clicked(event):
            exitclicked(Games,Buttons)

        if Buttons["home"].is_clicked(event):
            eggs = HomeReturn(Core_Ingredient, Add_Ins, Toppings,Games,Played,reset_constants,Buttons,eggs)

        if Games["level_playing"]:
            #controls key in sugar game
            if Games["sugar_game"]:
                sugarkeys(basket_rect,basket,basket_bottom,basket_left,basket_right,basket_top)

            #control keys in flour game
            flour_pour = flourkeys(Games,flour_pour,Played,reset_constants)
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if Games["toppings_time"]:
                    topclicking(Toppings, Games)

                if Games["milk_game"]:
                    milkclicking(milk_can)

                if Games["butter_game"]:
                    butter_text = butterclicking(Core_Ingredient,butter_back,Games,butter_text)

                elif not Games["toppings_time"]:
                    addclicking(Add_Ins, Games,reset_constants)

                #if ingredients have been clicked then minigame gets shown
                for name, item in Core_Ingredient.items():
                    if item.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"] and name != 'order':
                        Games["show_minigame"] = True
                        if not Played[f"{name}_played"]:
                            Games[f"{name}_game"] = True
                        elif Played[f"{name}_played"]:
                            Games["already_played"] = True
                        if name == "sugar":
                                basket_rect.topleft = (width/2-(basket.get_width()/2),500)

                if current_level.order.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"]:
                    Games["order_open"] = True 

        if event.type == pygame.MOUSEBUTTONUP:
            if Buttons["exit_button"].is_clicked_up:
                Games["clicked_button"] = False 

        ovenclicking(Games,Played,Buttons)

    if Games["show_home"]:
        Money,balance_text = homescreen(Games, minigame, minigame_rect,levels,Add_Ins,Toppings,Money,balance_text,Buttons)

    if Games["level_playing"]:
        if not Games["toppings_time"]:
            screen.blit(background, (0,0))
            Buttons["next"].draw(screen)
            HomeButton(Buttons, Games)
            for name, item in Core_Ingredient.items():
                item.draw(screen)

            if reset_constants["bowl_color"][1]:
                pygame.draw.circle(screen,reset_constants["bowl_color"][1], (800,580), reset_constants["bowl_r"][1])

            for name, item in Add_Ins.items():
                item.draw(screen)
                item.not_owned(screen)

            current_level.order.draw(screen)
            current_level,levels,eggs = nextclicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)

            if Games["show_minigame"]:
                screen.blit(minigame,minigame_rect)
                Buttons["exit_button"].draw(screen)
                if Games["not_owned_mini"]:
                    screen.blit(not_owned_text, (550,440))

            if Games["order_open"]:
                order_texts = order_recipe(order_texts, current_level, Games, Buttons)

            if Games["eggs_game"]:
                eggcontrols(basket,basket_rect,minigame_rect,basket_bottom,basket_left,basket_right,basket_top,eggs)
                egg_text = egg_collisions(eggs,basket_left,basket_right,basket_bottom,basket_top,height,Core_Ingredient,Games,Played,egg_text,reset_constants)

            if Games["milk_game"]:
                milk_text = milk_game_controls(milk_can,Core_Ingredient,Games,Played,milk_text,reset_constants)

            if Games["flour_game"]:
                flour_right,flour_text = flourfalling(flour_right,flour_pour,Core_Ingredient,sieve,sieve_rect,flour_complete,flour_complete_rect,flour_text,reset_constants)

            if Games["sugar_game"]:
                sugar_text,salt_text = sugarcontrols(basket_top,basket_left,basket_right,Games,Played,Core_Ingredient,sugar_text,salt_text,reset_constants)

            if Games["butter_game"]:
                butter_back = pygame.draw.rect(screen, (255, 253, 116), [width/2-250,reset_constants["butter_back_y"][1],500,200,])
                fallen_butter = butterdrawing(current_level,Games,Played,fallen_butter,butter_text,Core_Ingredient,reset_constants)
            
            if Games["add_coloring"]:
                choosecolor(Color_Buttons,Games,Add_Ins,reset_constants)

            if Games["already_played"]:
                screen.blit(already_played_text, (680,440))

            if Games["oven_game"]:
                ovendraw(oven,oven_rect,reset_constants,Games,Buttons)
                current_level,levels,eggs = nextclicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)
                HomeButton(Buttons, Games)

            add_top_draw(Add_Ins,Toppings,Games)

            if current_level == levels["tutorial"]:
                tutorial_process(Games,Played,Add_Ins,Toppings) 

        elif Games["toppings_time"]:
            screen.blit(traybackground, (0,0))
            screen.blit(reset_constants["cookies"][1], (0,0))
            Buttons["next"].draw(screen)
            current_level.order.draw(screen)
            for name, item in Toppings.items():
                item.draw(screen)
                item.not_owned(screen)
            if Games["show_minigame"]:
                screen.blit(minigame,minigame_rect)
                Buttons["exit_button"].draw(screen)
                if Games["not_owned_mini"]:
                    screen.blit(not_owned_text, (550,440))
            if Games["order_open"]:
                order_texts = order_recipe(order_texts, current_level, Games, Buttons) 
            HomeButton(Buttons, Games)
            add_top_draw(Add_Ins,Toppings,Games)
            if Games["add_icing"]:
                chooseicing(Color_Buttons,Games,Toppings)

            if current_level == levels["tutorial"]:
                tutorial_process(Games,Played,Add_Ins,Toppings)
            current_level,levels,eggs = nextclicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)
            if Games["finished_screen"]:
                screen.blit(minigame,minigame_rect)
                Money = compare_results(current_level,Core_Ingredient,Add_Ins,Toppings, Money,Games,reset_constants)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit