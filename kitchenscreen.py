import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))

#basic initializations
font = pygame.font.Font(None, 30)
basic_initializations = {}
already_played_text = font.render("Ingredient already added", True, (0,0,0))
background = pygame.image.load("assets/Kitchen.png").convert()
minigame = pygame.image.load("assets/minigame.png").convert_alpha()
minigame_rect = minigame.get_rect(topleft=((1600/2)-minigame.get_width()/2,(900/2)-minigame.get_height()/2))
traybackground = pygame.image.load("assets/traybackground.png").convert_alpha()
cookies = pygame.image.load("assets/Cookies.PNG").convert_alpha()
cookieRBG = (0,0,0)

#Ingredient class and initialization
class Ingredient:
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
        surface.blit(self.image, self.image_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
class Core(Ingredient):
    def __init__(self, path, x, y,expected=None):
        super().__init__(path, x, y)
        if expected:
            self.expected_value = expected
        self.achieved_value = 0

class Topping(Ingredient):
    def __init__(self, path, x,y,show_img = None,rw = None, rh =None):
        super().__init__(path, x, y, rw, rh)
        self.owned = False
        self.added = False
        self.color = ""
        self.expect_rgb = [0,0,0,0]
        self.achieve_rgb = [0,0,0,0]
        if show_img:
            self.show_img = pygame.image.load(show_img).convert_alpha()
        
    def not_owned(self,surface):
        if not self.owned:
            surface.blit(self.darken,self.darken_rect)
            surface.blit(self.lock, self.lock_rect)

Add_Ins = {"food coloring": Topping("assets/coloring.png",0,310), 
           "chocolate chips": Topping("assets/chocchips.jpg",170,310,"assets/ChocChipAdd.PNG"), 
           "sprinkles": Topping("assets/sprinkles.jpg",0,460,"assets/SprinkleAdd.PNG"), 
           "oats": Topping("assets/oats.jpg",170,460,"assets/OatsAdd.PNG"), 
           "peanuts": Topping("assets/peanuts.jpg",0,610,"assets/PeanutAdd.PNG"), 
           "pistachios": Topping("assets/pistachios.jpg",170,610,"assets/PistachioAdd.PNG"), 
           "matcha": Topping("assets/matcha.jpg",0,760), 
           "raisins": Topping("assets/raisins.jpg",170,760,"assets/RaisinsAdd.PNG"), 
        }

Toppings = {"icing": Topping("assets/icing.jpg",0,310,"assets/IcingTop.PNG"), 
           "chocolate chips": Topping("assets/chocchips.jpg",0,510,"assets/ChocChipTop.PNG",210,180), 
           "sprinkles": Topping("assets/sprinkles.jpg",0,710,"assets/SprinkleTop.PNG",210,180),
           "colored sugar": Topping("assets/coloredsugar.jpg",340,0,"assets/ColoredSugarTop.PNG"), 
           "peanuts": Topping("assets/peanuts.jpg",547,0,"assets/PeanutTop.PNG",190,202), 
           "pistachios": Topping("assets/pistachios.jpg",754,0,"assets/PistachioTop.PNG",190,202), 
           "marshmallows": Topping("assets/marshmallows.jpg",961,0,"assets/MarshmallowTop.PNG"), 
           "raisins": Topping("assets/raisins.jpg",1168,0,"assets/RaisinsTop.PNG",190,202,), 
           "pretzels": Topping("assets/pretzels.jpg",1381,0,"assets/PretzelsTop.PNG"),
           "strawberries": Topping("assets/strawberries.jpg",1381,230,"assets/StrawberriesTop.PNG"), 
           "syrup": Topping("assets/syrup.jpg",1381,455,"assets/SyrupTop.PNG"), 
           "coconut flakes": Topping("assets/coconut.webp",1381,685,"assets/CoconutTop.PNG"),
        }

Add_Ins["food coloring"].owned = True
Add_Ins["chocolate chips"].owned = True
Toppings["icing"].owned = True
Toppings["chocolate chips"].owned = True

#home screen
class Button:
    def __init__(self,w=100,h=100,x=100,y=100,image=None, name = None):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.image_rect = self.image.get_rect(center = (x,y))
        self.text = None
        if name:
            self.text = font.render(f'{name}', True, (0,0,0))
            self.text_rect = self.text.get_rect(center=(x,y))
    
    def draw(self, surface):
        surface.blit(self.image, self.image_rect)
        if self.text:
            surface.blit(self.text, self.text_rect)

    def is_clicked_up(self, event):
        return event.type == pygame.MOUSEBUTTONUP and self.image_rect.collidepoint(event.pos)
    
    def is_clicked(self,event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
level_button = Button(400,100,width/2,height/2 - 50,'assets/minigame.png', "Levels")
shop_button = Button(400,100,width/2,height/2 +75,'assets/minigame.png',"Shop")
play_button = Button(400,100,width/2,height/2 +200,'assets/minigame.png',"Play")
tutorial_button = Button(400,100,width/2,height/2 +325,'assets/minigame.png',"Tutorial")
exit_button = Button(55,55,minigame_rect.x+27, minigame_rect.y+28,'assets/exit.png')
home = Button(86,83,418,841,"assets/home.png")
next = Button(142,93,1146,846,"assets/nextbutton.png")

Color_Buttons = {
    "red": Button(100,100,400,400,"assets/red.png","Red"),
    "green": Button(100,100,400,400,"assets/green.png","Green"),
    "blue": Button(100,100,400,400,"assets/blue.png","Blue"),
}

def HomeButton(button, game, topping):
    if game["oven_game"]:
        button.image_rect.x = 950
    elif topping:
        button.image_rect.x = 300
    else:
        button.image_rect.x = 418
    button.draw(screen)

def HomeReturn(oven, returnhome, currentscreen, current,topping, add, top,games,played):
    currentscreen = False
    returnhome = True
    topping = False
    played["oven_played"] = False
    oven = False
    exitclicked(games)
    for name,item in current.core_ingredients.items():
        item.achieved_value = 0
        if name == "butter":
            item.achieved_value = []
        item.added = False
    for name,item, in add.items():
        item.added = False
    for name,item, in top.items():
        item.added = False
    return topping, returnhome, currentscreen, oven, played


def exitclicked(games):
    for name,item in games.items():
        games[name] = False
    games["clicked_button"] = True

class level:
    def __init__(self,n):
        self.core_ingredients = {}
        self.add_ins = {}
        self.toppings = {}
        self.order = None
        self.stars = 5
        self.expectedRGB = [0,0,0,0]
        self.achievedRGB = [0,0,0,0]
        self.n = n
        self.baked = 0
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

    def draw(self, surface):
        surface.blit(self.image, self.image_rect)
        surface.blit(self.text, self.text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.image_rect.collidepoint(event.pos)
    
    def clickedup(self, event):
        return event.type == pygame.MOUSEBUTTONUP and self.image_rect.collidepoint(event.pos)

completed_levels = {}
levels = {"tutorial": level(0)
          }

tutorial_ingredients = {"order": Core("assets/order.png",0,0), 
               "butter" : Core("assets/buttertray.png",342,2,[[550,500],[800,400], [1050,500], [925,600], [675,600]]),
               "eggs" : Core("assets/eggtray.png",810,0,2),
               "flour" : Core("assets/flour.png",1275,13,500),
               "sugar" : Core("assets/sugar.png",1275,320,300),
               "milk" : Core("assets/milk.png",1275,620,2)
        }
levels["tutorial"].core_ingredients = {"eggs": tutorial_ingredients["eggs"],
                                       "milk": tutorial_ingredients["milk"],
                                       "flour": tutorial_ingredients["flour"],
                                       "sugar": tutorial_ingredients["sugar"],
                                       "butter": tutorial_ingredients["butter"]}

levels["tutorial"].order = tutorial_ingredients["order"]
levels["tutorial"].add_ins = {'food coloring': Add_Ins["food coloring"],
                              'chocolate chips': Add_Ins["chocolate chips"]}
levels["tutorial"].toppings = {"icing": Toppings['icing'],
                               "chocolate chips": Toppings['chocolate chips']}

current_level = levels["tutorial"]

def homescreen(levelbutton, shop, play, tut, games, miniimage, minirect, exit,leveldict):
    screen.fill((225, 150, 164))
    levelbutton.draw(screen)
    shop.draw(screen)
    play.draw(screen)
    tut.draw(screen)

    if games["show_minigame"]:
        screen.blit(miniimage,minirect)
        exit.draw(screen)

    if games["show_levels"]:
        for name, thislevel in leveldict.items():
            thislevel.draw(screen)

def addlevel(leveldict,completed,adds,tops):
    if len(completed) <= len(leveldict) and len(leveldict) > 0:
        leveldict[len(completed)] = level(len(completed))
        Ingredients = {"order": Core(None,0,0), 
               "butter" : Core(None,342,2,[[randint(550,700),randint(400,500)],[randint(700,850),randint(400,500)], [randint(850,1050),randint(400,500)], [randint(800,1050),randint(500,600)], [randint(550,800),randint(500,600)]]),
               "eggs" : Core(None,810,0,randint(1,5)),
               "flour" : Core(None,1275,13,690- randint(400,690) * 3),
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
        
        leveldict[len(completed)].order = Ingredients["order"]
        for name, item in adds.items():
            if randint(0,1) == 1:
                if item.owned and name != "food coloring":
                    leveldict[len(completed)].add_ins[name] = Adds[name]
                if item.owned and name == "food coloring":
                    for shade in Colors:
                        if randint(0,1) == 1:
                            leveldict[len(completed)].add_ins[f"{shade} food coloring"] = Adds[name]
                            leveldict[len(completed)].expectedRGB[Colors.index(shade)] += 50

        for name, item in tops.items():
            if randint(0,1) == 1:
                if item.owned and name != "icing":
                    leveldict[len(completed)].toppings[name] = Tops[name]
                if item.owned and name == "icing":
                    chosen_color = randint(0,2)
                    Tops[name].expect_rgb[chosen_color] += 50
                    Tops[name].color = Colors[chosen_color]
                    leveldict[len(completed)].toppings[name] = Tops[name]

    return leveldict

def level_clicking(button,event,games,leveldict,playing,current):
    if button.is_clicked(event) and not games["show_minigame"]:
        games["show_levels"] = True
        games["show_minigame"] = True

    for name, num in leveldict.items():
        if num.clicked(event) and not playing:
            games["clicked_button"] = True
            current = num
            playing = True
            games["show_minigame"] = False
        
        if num.clickedup(event):
            clicked = False
            games["show_levels"] = False

    return playing, current

not_owned_text = font.render("Ingredient Not Owned. Would you like to purchase?", True, (0,0,0))
not_owned_mini = False

def addclicking(adds, current,toptime, games,own,colors):
    color_order = ["red", "green", "blue"]
    for name, item in adds.items():
        if item.clicked(event): 
            if item.owned and not toptime:
                if name in current.add_ins:
                    current.add_ins[name].added = True
                    item.added = True
                if name == "food coloring":
                    games["show_minigame"] = True
                    for shade, button in colors.items():
                        button.draw(screen)
                        if button.is_clicked(event):
                            current.achievedRGB[color_order.index(shade)] += 50
                            item.added = True
                else:
                    item.added = True
            if not item.owned and not toptime:
                own = True
    return own

def topclicking(tops, current,toptime,games,own, colors):
    color_order = ["red", "green", "blue"]
    rgb = [0,0,0,0]
    for name, item in tops.items():
        if item.clicked(event): 
            if item.owned:
                if name in current.toppings:
                    current.toppings[name].added = True
                    item.added = True
                if name == "icing":
                    games["show_minigame"] = True
                    for shade, button in colors.items():
                        button.draw(screen)
                        if button.is_clicked(event):
                            rgb[color_order.index(shade)] += 50
                            item.added = True
                            current.toppings[name].achieve_rgb = rgb
                else:
                    item.added = True
            if not item.owned:
                own = True
    return own

def add_top_draw(adds,tops,games,own,text,cookie_img,current):
    for name, item in adds.items():
        if name == "matcha" and item.added:
            g+=50
        if name != "food coloring" and name!= "matcha" and item.added and toppings_time:
            screen.blit(item.show_img, (0,0))
        if name == "food coloring":
            cookie_img.fill(tuple(current.achievedRGB), special_flags=pygame.BLEND_RGBA_ADD)
    for name, item in tops.items():
        if name == "icing" and item.added:
            item.show_img.fill(tuple(current.toppings[name].achieve_rgb), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(item.show_img, (0,0))
        if name != "icing" and item.added:
            screen.blit(item.show_img, (0,0))
        if own:
            games["show_minigame"] = True
            screen.blit(text, (550,440))

def compare_results(current, adds,tops):
    wrong = {}
    if current.stars >0:
        for name,item in current.core_ingredients.items():
            if item.achieved_value > item.expected_value +20 or item.achieved_value < item.expected_value -20:
                wrong.append('Incorrect value of ingredients added')
        for name,item in current.add_ins.items():
            if not item.added:
                wrong.append('Missing ingredient')
        for add, ingredient in adds.items():
            if add not in current.add_ins and add.added:
                wrong.append('Incorrect ingredient added')
        for name,item in current.toppings.items():
            if not item.added:
                wrong.append('Missing ingredient')
        for top, ingredient in tops.items():
            if add not in current.add_ins and add.added:
                wrong.append('Incorrect topping added')

#egg game initializations
egg_fallen = 0
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

#egg class and initialization
class egg:
    def __init__(self, w, h):
        self.x = randint(minigame_rect.x + 50,minigame_rect.x + minigame.get_width()-50)
        self.y = randint(-550,-75)
        self.w = w
        self.h = h
        self.original_image = pygame.image.load('assets/egg.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (w,h))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.detect = False
        self.y_velocity = randint(2,4)
        self.collected = False
        self.fallen = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.y_velocity

eggs = [egg(50,75) for i in range(5)]
egg_text = font.render(f"Eggs: {current_level.core_ingredients["eggs"].achieved_value}", True, (0,0,0))

#updates egg position as they fall and increments count when they fall in the basket
def egg_collisions(egg_list,left,right,bottom,top,length,current,fallen,games,played,text):
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
            current.core_ingredients["eggs"].achieved_value += 1
            text = font.render(f"Eggs: {current.core_ingredients["eggs"].achieved_value}", True, (0,0,0))
            egg.collected = True
            fallen += 1
        if egg.rect.top >= length and not egg.fallen:
            egg.fallen = True
            fallen += 1
        
        if fallen == 5:
            games["eggs_game"] = False
            played["eggs_played"] = True
            games["show_minigame"] = False

        screen.blit(text,(1100,150))
    return fallen, text

def basket_update(rect,bottom,left,right,top):
    bottom.update(rect.x, rect.y+rect.height-10, rect.width, 10)
    left.update(rect.x, rect.y, 10, rect.height)
    right.update(rect.x+rect.width-10, rect.y, 10, rect.height)
    top.update(rect.x+10, rect.y, rect.width-20, 10)

#checks if eggs are in basket
    
def eggcontrols(basket,basketrect,minirect,bottom,left,right,top,egglist,current):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basketrect.x > minirect.x:
        basketrect.x -= 9
    if keys[pygame.K_RIGHT] and basketrect.x < 800+minirect.width/2 - basketrect.width:
        basket_rect.x += 9
    basket_update(basketrect, bottom, left,right,top)

    screen.blit(basket, basketrect)

    for egg in egglist:
        egg.draw(screen)
#Bottle class and initialization

class Bottle:
    def __init__(self, x, y, w, h):
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
        surface.blit(self.image, self.rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def clickedup(self,event):
        return event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos)

    def toggle_rotation(self):
        self.turned = not self.turned
        angle = 45 if self.turned else -45
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

milk_can = Bottle(930, 230, 100,150)
milk_h = 0
milk_y = 690

milk_text = font.render(f"Volume: {current_level.core_ingredients["milk"].achieved_value}", True, "Black")

def milkclicking(can):
    if can.clicked(event):
        can.toggle_rotation()
        if not can.poured and can.turned:
            can.poured = True


def milk_game_controls(can,h,y,current,games,played,text):
    can.draw(screen)
    milk_cup = pygame.draw.rect(screen, "black", [700, 400, 300, 300], 10)
    milk_fill = pygame.draw.rect(screen, "white", [710, y, 280, h])
    
    if can.turned:
        milk_liquid = pygame.draw.rect(screen, "white", [840,213,10,477])
        h+=1
        y-=1
        current.core_ingredients["milk"].achieved_value += 2
        text = font.render(f"Volume: {current.core_ingredients["milk"].achieved_value}", True, "Black")

    if can.turned and current.core_ingredients["milk"].achieved_value >= 560:
        can.toggle_rotation()
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    if not can.turned and can.poured:
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    screen.blit(text, (1100,150))

    return h,y,text

#flour minigame initialization
sieve = pygame.image.load("assets/sieve.png").convert_alpha()
sieve = pygame.transform.scale(sieve, (250,150))
sieve_rect = sieve.get_rect(center=(width/2,height/2-200))
flour_right = True
sieve_y = 690
sieve_x = 600
sieve_h = 0
flour_front_w = 150
flour_front_x = sieve_rect.x + 75
flour_pour = False
flour_complete = pygame.image.load("assets/checkbox.png").convert()
flour_complete = pygame.transform.scale(flour_complete, (100,100))
flour_complete_rect = flour_complete.get_rect(center = (width/2+350,height/2-150))
flour_text = font.render(f"Volume: {int(current_level.core_ingredients["flour"].achieved_value/100)}", True, "Black")

def flourfalling(right,x,pour,h,flourx,flourw,rect,y,current,image,imagerect,complete,completerect,flour_volume_text):
    screen.blit(image,imagerect)
    cup = pygame.draw.rect(screen, "black", [x, 400, 300, 300], 10)
    fill = pygame.draw.rect(screen, "white", [x+10, y, 280, h])
    screen.blit(complete,completerect)
    screen.blit(flour_volume_text,(1100,150))

    if right:
        x += 5
    else:
        x -= 5
    if x >= 1000:
        right = False
    if x <= 300:
        right = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        pour = True

    if pour and h < 290:
        flourfront = pygame.draw.rect(screen, "white", [flourx,rect.y + 150,flourw,800])
        flourback = pygame.draw.rect(screen, "white", [rect.x + 75,rect.y + 150,150, cup.y - rect.y + 140])
        if cup.x <= flourback.x + 150 and cup.x +300 >= flourback.x:
            if cup.x > rect.x and cup.x < rect.x + 225:
                flourw = cup.x - rect.x - 75
                flourx = rect.x + 75
            elif cup.x < rect.x and cup.x +300 > rect.x + 75:
                flourw = rect.x -75 - cup.x
                flourx = cup.x + 300
            else:
                flourw = 150
                flourx = rect.x + 75
            h+= abs(cup.y - rect.y)/300
            y-= abs(cup.y - rect.y)/300
            current.core_ingredients["flour"].achieved_value += abs(cup.y - rect.y)
            flour_volume_text = font.render(f"Volume: {int(current.core_ingredients["flour"].achieved_value/100)}", True, "Black")

    return x,h,y,right,flourx,flourw,flour_volume_text

def flourkeys(games,pour,played):
    flour_keys = pygame.key.get_pressed()
    if flour_keys[pygame.K_DOWN]:
        pour = True
    else: 
        pour = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if flour_complete_rect.collidepoint(mouse_pos):
            games["flour_game"] = False
            played["flour_played"] = True
            games["show_minigame"] = False
    return pour

#Sugar minigame class

class SugarSalt:
    def __init__(self, y, type, x):
        self.x = x
        self.y = y
        self.type = type
        if self.type == "sugar":
            self.original_image = pygame.image.load('assets/sugarimage.png').convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (75,75))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.type == "salt":
            self.original_image = pygame.image.load('assets/salt.png').convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (75,100))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 3

def sugarkeys(rect,container,bottom,left,right,top):
    sugar_keys = pygame.key.get_pressed()
    if sugar_keys[pygame.K_LEFT] and rect.x != width/2-(container.get_width()/2)-400:
        rect.x -= 400
    if sugar_keys[pygame.K_RIGHT] and rect.x != width/2-(container.get_width()/2)+400:
        rect.x += 400
    basket_update(rect, bottom, left,right,top)

#sugar salt lane randomization
def sugar_salt_coordinates(sugar_salts_list):
    for i in range(5):
        nums = [375,width/2-37,1150]
        chosen_x = nums[randint(0,2)]
        sugar_salts_list.append(SugarSalt(-50-(i*200),"sugar",chosen_x))
        nums.remove(chosen_x)
        chosen_x = nums[randint(0,1)]
        sugar_salts_list.append(SugarSalt(-50-(i*200),"salt", chosen_x))

#sugar minigame initializations
basket_rect.topleft = (width/2-(basket.get_width()/2),500)
SugarSalts = []

sugar_salt_coordinates(SugarSalts)
current_level.core_ingredients["sugar"].achieved_value = [0,0]
sugar_text = font.render(f"Sugar Collected: {current_level.core_ingredients["sugar"].achieved_value[0]}", True, "Black")
salt_text = font.render(f"Salt Collected: {current_level.core_ingredients["sugar"].achieved_value[1]}", True, "Black")

def sugarcontrols(sugarlist,top,left,right,games,played,current,sugarstext,saltstext):
    for ingredient in sugarlist:
        ingredient.update()
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "sugar":        
            current.core_ingredients["sugar"].achieved_value[0] += 1
            sugarlist.remove(ingredient)
            sugarstext = font.render(f"Sugar Collected: {current.core_ingredients["sugar"].achieved_value[0]}", True, "Black")
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "salt":        
            sugarlist.remove(ingredient)
            current.core_ingredients["sugar"].achieved_value[1] += 1
            saltstext = font.render(f"Salt Collected: {current.core_ingredients["sugar"].achieved_value[1]}", True, "Black")
        if ingredient.rect.y >= 900:
            sugarlist.remove(ingredient)

    for ingredient in sugarlist:
        ingredient.draw(screen)
    screen.blit(basket, basket_rect)

    screen.blit(sugarstext,(950,150))
    screen.blit(saltstext,(950,200))

    if not sugarlist:
        games["sugar_game"] = False
        played["sugar_played"] = True
        games["show_minigame"] = False

    return sugarlist,sugarstext,saltstext

#butter game initialization

current_level.core_ingredients["butter"].achieved_value = []
butter_back_y = height/2-50
fallen_butter = []

#shoelace formula
def shoelace(vertices):
    total = 0
    for i in range(len(vertices)):
        butter_xy = vertices[i%len(vertices)][0]*vertices[(1+i)%len(vertices)][1]
        butter_yx = vertices[i%len(vertices)][1]*vertices[(1+i)%len(vertices)][0]
        total += butter_xy-butter_yx
    return abs(total)

butter_expected_total = shoelace(current_level.core_ingredients["butter"].expected_value)
butter_back = pygame.Rect([width/2-250,butter_back_y,500,200,])
butter_text = font.render(f"Current volume: 0", True, "black")

def butterclicking(current,back,games,text):
    if len(current.core_ingredients["butter"].achieved_value)<=4:
        mouse_pos = event.pos
        if back.collidepoint(mouse_pos) and not games["clicked_button"]:
            current.core_ingredients["butter"].achieved_value.append(pygame.mouse.get_pos())

    text = font.render(f"Current volume: {int(shoelace(current.core_ingredients["butter"].achieved_value)/1000)}", True, "black")
    return text

def butterdrawing(current,y,games,played,fallen,text):
    for i in range(5):
        pygame.draw.line(screen, "green", (current.core_ingredients["butter"].expected_value[i%5][0],current.core_ingredients["butter"].expected_value[i%5][1]),(current.core_ingredients["butter"].expected_value[(i+1)%5][0],current.core_ingredients["butter"].expected_value[(i+1)%5][1]),10)
    for i in range(len(current.core_ingredients["butter"].achieved_value)):
        pygame.draw.circle(screen,"black",current.core_ingredients["butter"].achieved_value[i],2)
        if len(current.core_ingredients["butter"].achieved_value) >= 2:
            pygame.draw.line(screen, "black", current.core_ingredients["butter"].achieved_value[i%(len(current.core_ingredients["butter"].achieved_value))],current.core_ingredients["butter"].achieved_value[(i+1)%len(current.core_ingredients["butter"].achieved_value)],5)

    if len(current.core_ingredients["butter"].achieved_value) == 5 and not fallen:
        fallen = [list(x) for x in current.core_ingredients["butter"].achieved_value]

    if len(current.core_ingredients["butter"].achieved_value) == 5:
        pygame.draw.polygon(screen,(200,200,200),fallen)
        pygame.draw.polygon(screen,(255, 253, 116),current.core_ingredients["butter"].achieved_value)
        for i in range(5):
            fallen[i][1] += 2
            current.core_ingredients["butter"].expected_value[i][1] += 2
        y += 2

    if butter_back.y >= 900:
        games["butter_game"] = False
        played["butter_played"] = True
        games["show_minigame"] = False

    screen.blit(text,(950,150))
    
    return y,fallen

order_texts = {}

def order_recipe(texts, current, screen, games, exit):
    games["show_minigame"] = True
    exit.draw(screen)
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
    texts["top"] = font.render(f"Toppings:", True, "Black")
    screen.blit(texts["top"],(800,150))
    for i, (name, expected) in enumerate(current.toppings.items()):
        if name == "icing":
            texts[name] = font.render(f"{item.color} {name}", True, "Black")
        else:
            texts[name] = font.render(f"{name}", True, "Black")
        screen.blit(texts[name],(800,150+(i+1)*40))
    return texts

#Oven initializations
oven = pygame.image.load("assets/oven.png").convert_alpha()
oven_rect = oven.get_rect(center = (500,450))
startbutton = pygame.image.load("assets/startbutton.png").convert()
startbutton_rect = startbutton.get_rect(center = (1200,450))
stopbutton = pygame.image.load("assets/stopbutton.png").convert()
stopbutton_rect = stopbutton.get_rect(center = (1200,450))
oven_width = 0
oven_r = 255
oven_g = 255
oven_b = 255

def ovendraw(image,image_rect,r,g,b,w,startshow,start,start_rect,stop,stop_rect,next_image,current):
    screen.fill((225, 150, 164))
    screen.blit(image,image_rect)
    home.draw(screen)
    oven_ready_bar = pygame.draw.rect(screen, (r,g,b),[270,111,w, 88])
    if startshow:
        screen.blit(start,start_rect)
    elif oven_playing:
        screen.blit(stop,stop_rect)
        if w<472:
            w += 1
            if r > 0 and b > 0:
                r -= 0.5
                b -= 0.5
        elif r < 255 and g>0:
            r += 2
            g -=2
    else:
        next_image.draw(screen)
    current.baked = r
    return r,g,b,w

def ovenclicking(games,played,startshow,toppings,start,playing,next_button):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if next_button.is_clicked(event) and not played["oven_played"]:
            games["oven_game"] = True
            startshow = True
        elif next_button.is_clicked(event) and played["oven_played"]:
            toppings = True
            games["oven_game"] = False

        if start.collidepoint(mouse_pos) and not played["oven_played"] and startshow:
            games["clicked_button"] = True
            startshow = False
            playing = True
        
        elif stopbutton_rect.collidepoint(mouse_pos) and playing and not games["clicked_button"]:
            played["oven_played"] = True
            playing = False

    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = event.pos
        if start.collidepoint(mouse_pos):
            games["clicked_button"] = False

    
    return startshow,toppings,playing

def go_to_finished(next_button, games, completed_list, level_list, current, played,add,top,topping,oven):
    if next_button.is_clicked(event) and not games["finished_screen"]:
        games["finished_screen"] = True
    if next_button.is_clicked(event) and games["finished_screen"]:
        games["finished_screen"] = False
        completed_list[len(completed_list)] = current
        level_list = addlevel(level_list,completed_list,add,top)
        current = level_list[len(completed_list)]
        topping = False
        played["oven_played"] = False
        oven = False
        exitclicked(games)
        for name,item in current.core_ingredients.items():
            item.achieved_value = 0
            if name == "butter":
                item.achieved_value = []
            item.added = False
        for name,item in add.items():
            item.added = False
        for name,item in top.items():
            item.added = False
    return topping,oven,current,level_list


#boolean initializations
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
         "finished_screen": False
         }

Played = {"eggs_played": False,
          "milk_played": False,
          "flour_played": False,
          "sugar_played": False,
          "butter_played": False,
          "oven_played": False}

show_home = True
level_playing = False
oven_playing = False
startbutton_show = False
toppings_time = False
running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #controls key in sugar game
        if Games["sugar_game"]:
            sugarkeys(basket_rect,basket,basket_bottom,basket_left,basket_right,basket_top)

        level_playing, current_level = level_clicking(level_button,event,Games,levels,level_playing,current_level)

        #control keys in flour game
        flour_pour = flourkeys(Games,flour_pour,Played)

        #If exit is pressed minigame disappears
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event):
                exitclicked(Games)
            
            if home.is_clicked(event):
                toppings_time, show_home, level_playing, oven_game = HomeReturn(oven, show_home, level_playing, current_level,toppings_time, Add_Ins, Toppings,Games,Played)

            if toppings_time:
                not_owned_mini = topclicking(Toppings,current_level,toppings_time, Games,not_owned_mini,Color_Buttons)

            if Games["milk_game"]:
                milkclicking(milk_can)

            if Games["butter_game"]:
                butter_text = butterclicking(current_level,butter_back,Games,butter_text)

            else:
                not_owned_mini = addclicking(Add_Ins,current_level,toppings_time, Games,not_owned_mini,Color_Buttons)

            #if ingredients have been clicked then minigame gets shown
            for name, item in current_level.core_ingredients.items():
                if item.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"]:
                    Games["show_minigame"] = True
                    if not Played[f"{name}_played"]:
                        Games[f"{name}_game"] = True
                    if name == "sugar":
                            basket_rect.topleft = (width/2-(basket.get_width()/2),500)
                    elif Played[f"{name}_played"]:
                        Games["already_played"] = True

            if current_level.order.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"]:
                Games["order_open"] = True 

        if event.type == pygame.MOUSEBUTTONUP:
            if exit_button.is_clicked_up:
                Games["clicked_button"] = False   

        startbutton_show,toppings_time,oven_playing = ovenclicking(Games,Played,startbutton_show,toppings_time,startbutton_rect,oven_playing,next)

    if show_home:
        homescreen(level_button, shop_button, play_button, tutorial_button, Games, minigame, minigame_rect, exit_button,levels)

    if level_playing:
        screen.blit(background, (0,0))
        next.draw(screen)
        HomeButton(home, Games,toppings_time)
        for name, item in current_level.core_ingredients.items():
            item.draw(screen)

        for name, item in Add_Ins.items():
            item.draw(screen)
            item.not_owned(screen)

        current_level.order.draw(screen)

        if Games["show_minigame"]:
            screen.blit(minigame,minigame_rect)
            exit_button.draw(screen)

        if Games["order_open"]:
            order_texts = order_recipe(order_texts, current_level, screen, Games, exit_button) 

        #egg minigame
        if Games["eggs_game"]:
            eggcontrols(basket,basket_rect,minigame_rect,basket_bottom,basket_left,basket_right,basket_top,eggs,current_level)
            egg_fallen,egg_text = egg_collisions(eggs,basket_left,basket_right,basket_bottom,basket_top,height,current_level,egg_fallen,Games,Played,egg_text)

        if Games["milk_game"]:
            milk_h,milk_y,milk_text = milk_game_controls(milk_can,milk_h,milk_y,current_level,Games,Played,milk_text)

        if Games["flour_game"]:
            sieve_x,sieve_h,sieve_y,flour_right,flour_front_x,flour_front_w,flour_text = flourfalling(flour_right,sieve_x,flour_pour,sieve_h,flour_front_x,flour_front_w,sieve_rect,sieve_y,current_level,sieve,sieve_rect,flour_complete,flour_complete_rect,flour_text)

        if Games["sugar_game"]:
            SugarSalts,sugar_text,salt_text = sugarcontrols(SugarSalts,basket_top,basket_left,basket_right,Games,Played,current_level,sugar_text,salt_text)

        if Games["butter_game"]:
            butter_back = pygame.draw.rect(screen, (255, 253, 116), [width/2-250,butter_back_y,500,200,])
            butter_back_y,fallen_butter = butterdrawing(current_level,butter_back_y,Games,Played,fallen_butter,butter_text)

        if Games["already_played"]:
            screen.blit(already_played_text, (680,440))

        if Games["oven_game"]:
            oven_r,oven_g,oven_b,oven_width= ovendraw(oven,oven_rect,oven_r,oven_g,oven_b,oven_width,startbutton_show,startbutton,startbutton_rect,stopbutton,stopbutton_rect,next,current_level)
            HomeButton(home, Games,toppings_time)

        add_top_draw(Add_Ins,Toppings,Games,not_owned_mini,not_owned_text,cookies,current_level)

        if toppings_time:
            screen.blit(traybackground, (0,0))
            screen.blit(cookies, (0,0))
            add_top_draw(Add_Ins,Toppings,Games,not_owned_mini,not_owned_text,cookies,current_level)
            next.draw(screen)
            for name, item in Toppings.items():
                item.draw(screen)
                item.not_owned(screen)
            HomeButton(home, Games,toppings_time)
            toppings_time,oven_playing,current_level,levels = go_to_finished(next, Games, completed_levels, current_level,levels, Played,Add_Ins,Toppings,toppings_time,oven_playing)
            if Games["finished_screen"]:
                Games["show_minigame"] == True


    pygame.display.flip()
    clock.tick(fps)

pygame.quit