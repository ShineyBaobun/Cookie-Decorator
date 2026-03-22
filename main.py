import pygame
from ButterGame import *
from EggGame import *
from FlourGame import *
from HomeScreen import * 
from MilkGame import *
from SugarGame import *
from Toppings import *
from OvenGame import *
from DataStorage import *

width = 1600
height = 900

pygame.init()

font = pygame.font.Font("assets/PixelFont.otf", 20)
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

Money = 100000

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
            tutorial_instructions(280,200,"Click order to see what ingredients to add",0)
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
            tutorial_instructions(280,200,"Click order to see what toppings to add",0)
        if played["order_opened"] and not games["added_icing"] and not games["show_minigame"]:
            tutorial_instructions(0,450,"Add food coloring",-58)
        if games["add_icing"] and games["show_minigame"]:
            tutorial_instructions(470,520,"Add red food coloring",-58)

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
            elif name == "food coloring":
                value = font.render(f"{expected.color} {name}", True, "Black")
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
                texts[name] = font.render(f"{expected.color} {name}", True, "Black")
            else:
                texts[name] = font.render(f"{name}", True, "Black")
            screen.blit(texts[name],(400,150+(i+1)*40))
    return texts

def next_clicking(games, played, current,level_list,completed_list,add,top,core,reset,buttons,egg_list):
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
                return current,level_list,egg_list,completed_list
            if not games["level_increased"]:
                completed_list += 1
                games["level_increased"] = True
            level_list = addlevel(level_list,completed_list,add,top,Core_Ingredient)
            current = level_list[completed_list]
            games["toppings_time"] = False
            egg_list = resetting_level(core, add, top,games,played,reset,buttons,egg_list,current)
            return current,level_list,egg_list,completed_list

    if buttons["next"].is_clicked_up(event):
        games["clicked_button"] = False

    return current,level_list,egg_list,completed_list

def add_screen(buttons,games,core,reset,adds):
    screen.blit(background, (0,0))
    buttons["next"].draw(screen)
    Home_Button(buttons, games,screen)
    for name, item in core.items():
        item.draw(screen)

    if reset["bowl_color"][1]:
        pygame.draw.circle(screen,reset["bowl_color"][1], (800,580), reset["bowl_r"][1])

    for name, item in adds.items():
        item.draw(screen)
        item.not_owned(screen)

def top_screen(trayback,reset,buttons,core,tops):
    screen.blit(trayback, (0,0))
    screen.blit(reset["cookies"][1], (0,0))
    buttons["next"].draw(screen)
    core['order'].draw(screen)
    for name, item in tops.items():
        item.draw(screen)
        item.not_owned(screen)

def draw_mini(mini_image,buttons,games,not_text):
    screen.blit(mini_image,(256,109))
    buttons["exit_button"].draw(screen)
    if games["not_owned_mini"]:
        screen.blit(not_text, (550,440))

logo = pygame.image.load('assets/logo.png').convert_alpha()
logo = pygame.transform.scale(logo, (513,242))
background = pygame.image.load("assets/Kitchen.png").convert()
minigame = pygame.image.load("assets/minigame.png").convert_alpha()
traybackground = pygame.image.load("assets/traybackground.png").convert_alpha()
already_played_text = font.render("Ingredient already added", True, (0,0,0))
balance_text = font.render(f"Balance: {Money}", True, "Black")
tutorial_arrow = pygame.image.load("assets/tutorial_arrow.png").convert_alpha

completed_levels = 0
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

levels["tutorial"].core_ingredients = {"butter" : Core(None,342,2,[[550,500],[800,400], [1050,500], [925,600], [675,600]]),
               "eggs" : Core(None,810,0,2),
               "flour" : Core(None,1275,13,500),
               "sugar" : Core(None,1275,320,3),
               "milk" : Core(None,1275,620,200)}

levels["tutorial"].order = Core(None,0,0)
levels["tutorial"].add_ins = {'chocolate chips': Topping(None,170,310)}
levels["tutorial"].toppings = {"icing": Topping(None,170,310),
                               "chocolate chips": Topping(None,0,510,None)}

levels["tutorial"].toppings["icing"].expect_rgb = [255,50,50]
levels["tutorial"].toppings["icing"].color = "red"

current_level = levels["tutorial"]

Buttons = {"level_button": Button(400,100,width/2,height/2 - 50,'assets/minigame.png', "Levels"),
           "shop_button": Button(400,100,width/2,height/2 +75,'assets/minigame.png',"Shop"),
           "play_button": Button(400,100,width/2,height/2 +200,'assets/minigame.png',"Play"),
           "tutorial_button": Button(400,100,width/2,height/2 +325,'assets/minigame.png',"Tutorial"),
           "NewGame": Button(400,100,width/2,height/2 -50,'assets/minigame.png',"New Game"),
           "StoredGame": Button(400,100,width/2,height/2 +50,'assets/minigame.png',"Load Stored Game"),
           "exit_button": Button(55,55,283,137,'assets/exit.png'),
           "home": Button(86,83,418,841,"assets/home.png"),
           "next": Button(142,93,1146,846,"assets/nextbutton.png"),
           "next_right": Button(142,93,1300,450,"assets/next_right.png"),
           "next_left": Button(142,93,300,450,"assets/next_left.png"),
           "buy_button": Button(75,50,800,450,"assets/next_left.png"),
           "startbutton": Button(523,178,1200,450,"assets/startbutton.png"),
           "stopbutton": Button(523,178,1200,450,"assets/stopbutton.png"),
           "flour_complete": Button(150,150,1150,300,"assets/checkbox.png")}

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

Basket = {"bottom": pygame.Rect(basket_rect.x,basket_rect.y+basket_rect.height-10,basket_rect.width,10),
          "left":pygame.Rect(basket_rect.x,basket_rect.y,10,basket_rect.height),
          "right": pygame.Rect(basket_rect.x+basket_rect.width-10,basket_rect.y,10,basket_rect.height),
          "top": pygame.Rect(basket_rect.x+10, 
                            basket_rect.y, 
                            basket_rect.width-20, 
                            10)}

eggs = [egg() for i in range(5)]
egg_text = font.render(f"Eggs: {Core_Ingredient["eggs"].achieved_value}", True, (0,0,0))

milk_can = Bottle(930, 230, 100,150)
milk_text = font.render(f"Volume: {Core_Ingredient["milk"].achieved_value}", True, "Black")

sieve = pygame.image.load("assets/sieve.png").convert_alpha()
sieve = pygame.transform.scale(sieve, (250,150))
sieve_rect = sieve.get_rect(center=(1600/2,900/2-200))

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
                   "butter_back_y": [900/2-50,900/2-50],
                   "oven_width": [0,0],
                   "oven_r": [255,255],
                   "oven_g": [255,255],
                   "oven_b": [255,255],
                   "cookies": [pygame.image.load("assets/Cookies.PNG").convert_alpha(),pygame.image.load("assets/Cookies.PNG").convert_alpha()]}

flour_right = True
flour_pour = False
flour_text = font.render(f"Volume: {int(Core_Ingredient["flour"].achieved_value/100)}", True, "Black")

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

game_chosen = False

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
         "level_increased": False
         }

Played = {"eggs_played": False,
          "milk_played": False,
          "flour_played": False,
          "sugar_played": False,
          "butter_played": False,
          "oven_played": False,
          "order_opened": False}

Loaded_Game = False
running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            Store_Data(levels,Money)

        if Games["show_home"] and not Games["level_playing"] and Loaded_Game:
            current_level = level_clicking(event,Games,levels,current_level,Buttons,Core_Ingredient)
            shop_clicking(Games,Buttons,event)

        if Buttons["exit_button"].is_clicked(event):
            exit_clicked(Games,Buttons)

        if Buttons["home"].is_clicked(event):
            eggs = Home_Return(Core_Ingredient, Add_Ins, Toppings,Games,Played,reset_constants,Buttons,eggs,current_level)

        if Games["level_playing"] and Loaded_Game:
            #controls key in sugar game
            if Games["sugar_game"]:
                sugar_keys(basket_rect,basket,Basket)

            #control keys in flour game
            flour_pour = flour_keys(Games,flour_pour,Played,reset_constants,event,Buttons)
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if Games["toppings_time"]:
                    top_clicking(Toppings, Games,event)

                if Games["milk_game"]:
                    milk_clicking(milk_can,event)

                if Games["butter_game"]:
                    butter_text = butter_clicking(Core_Ingredient,butter_back,Games,butter_text,event,font)

                elif not Games["toppings_time"]:
                    add_clicking(Add_Ins, Games,reset_constants,event)

                #if ingredients have been clicked then minigame gets shown
                for name, item in Core_Ingredient.items():
                    if item.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"] and name != 'order' and not Games["toppings_time"]:
                        Games["show_minigame"] = True
                        if not Played[f"{name}_played"]:
                            Games[f"{name}_game"] = True
                        elif Played[f"{name}_played"]:
                            Games["already_played"] = True
                        if name == "sugar":
                                basket_rect.topleft = (width/2-(basket.get_width()/2),500)

                if Core_Ingredient["order"].clicked(event) and not Games["show_minigame"] and not Games["clicked_button"]:
                    Games["order_open"] = True 

        if event.type == pygame.MOUSEBUTTONUP:
            if Buttons["exit_button"].is_clicked_up:
                Games["clicked_button"] = False 

        oven_clicking(Games,Played,Buttons,event)

    if not Loaded_Game:
        Money,Loaded_Game = Load_Data(levels,Money,Buttons,event,minigame,screen,Loaded_Game)

    else:

        if Games["show_home"] and not Games["toppings_time"]:
            Money,balance_text = homescreen(Games, minigame,levels,Add_Ins,Toppings,Money,balance_text,Buttons,event,screen,font,logo,Money)

        if Games["level_playing"]:
            if not Games["toppings_time"]:
                add_screen(Buttons,Games,Core_Ingredient,reset_constants,Add_Ins)

                current_level,levels,eggs,completed_levels = next_clicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)

                if Games["show_minigame"]:
                    draw_mini(minigame,Buttons,Games,not_owned_text)

                if Games["order_open"]:
                    order_texts = order_recipe(order_texts, current_level, Games, Buttons)

                if Games["eggs_game"]:
                    egg_controls(basket,basket_rect,Basket,eggs,screen)
                    egg_text = egg_collisions(eggs,Basket,Core_Ingredient,Games,Played,egg_text,reset_constants,screen,font)

                if Games["milk_game"]:
                    milk_text = milk_game_controls(milk_can,Core_Ingredient,Games,Played,milk_text,reset_constants,font,screen)

                if Games["flour_game"]:
                    flour_right,flour_text = flour_falling(flour_right,flour_pour,Core_Ingredient,sieve,sieve_rect,Buttons,flour_text,reset_constants,screen,font)

                if Games["sugar_game"]:
                    sugar_text,salt_text = sugar_controls(Basket,Games,Played,Core_Ingredient,sugar_text,salt_text,reset_constants,font,screen,basket,basket_rect)

                if Games["butter_game"]:
                    butter_back = pygame.draw.rect(screen, (255, 253, 116), [width/2-250,reset_constants["butter_back_y"][1],500,200,])
                    fallen_butter = butter_drawing(Games,Played,fallen_butter,butter_text,Core_Ingredient,reset_constants,screen,butter_back)
                
                if Games["add_coloring"]:
                    choose_color(Color_Buttons,Games,Add_Ins,reset_constants,event,screen)

                if Games["already_played"]:
                    screen.blit(already_played_text, (680,440))

                if Games["oven_game"]:
                    oven_draw(oven,oven_rect,reset_constants,Games,Buttons,screen)
                    current_level,levels,eggs,completed_levels = next_clicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)

                add_top_draw(Add_Ins,Toppings,Games,screen)

                if current_level == levels["tutorial"]:
                    tutorial_process(Games,Played,Add_Ins,Toppings) 

            elif Games["toppings_time"]:
                top_screen(traybackground,reset_constants,Buttons,Core_Ingredient,Toppings)

                if Games["show_minigame"]:
                    draw_mini(minigame,Buttons,Games,not_owned_text)

                if Games["order_open"]:
                    order_texts = order_recipe(order_texts, current_level, Games, Buttons) 

                Home_Button(Buttons, Games,screen)
                add_top_draw(Add_Ins,Toppings,Games,screen)

                if Games["add_icing"]:
                    choose_icing(Color_Buttons,Games,Toppings,event,screen)

                if current_level == levels["tutorial"]:
                    tutorial_process(Games,Played,Add_Ins,Toppings)

                current_level,levels,eggs,completed_levels = next_clicking(Games, Played, current_level, levels,completed_levels,Add_Ins,Toppings,Core_Ingredient,reset_constants,Buttons,eggs)
                if Games["finished_screen"]:
                    screen.blit(minigame,(256,109))
                    Money = compare_results(current_level,Core_Ingredient,Add_Ins,Toppings, Money,Games,reset_constants,font,screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit