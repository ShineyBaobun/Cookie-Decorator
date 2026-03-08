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
bowl_color = None
bowl_r = 150
Money = 50000
balance_text = font.render(f"Balance: {Money}", True, "Black")

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
        if not self.owned:
            surface.blit(self.darken,self.darken_rect)
            surface.blit(self.lock, self.lock_rect)
    
    def draw_description(self,descript):
        self.description = font.render(f"{self.name} costs {self.cost}", True, "Black")
        self.location = list(self.slide_pos)
        self.location[0] -= 100
        self.location[1] += 100
        screen.blit(self.description,tuple(self.location))

    def try_purchase(self,event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.buy_rect.collidepoint(event.pos)


Core_Ingredient = {"order": Core("assets/order.png",0,0), 
               "butter" : Core("assets/buttertray.png",342,2,[[550,500],[800,400], [1050,500], [925,600], [675,600]]),
               "eggs" : Core("assets/eggtray.png",810,0,2),
               "flour" : Core("assets/flour.png",1275,13,500),
               "sugar" : Core("assets/sugar.png",1275,320,300),
               "milk" : Core("assets/milk.png",1275,620,2)
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
        self.clicks = 0
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
next_right = Button(142,93,1300,450,"assets/next_right.png")
next_left = Button(142,93,300,450,"assets/next_left.png")
buy_button = Button(75,50,800,450,"assets/next_left.png")

Color_Buttons = {
    "red": Button(100,100,600,500,"assets/red.png","Red"),
    "green": Button(100,100,800,500,"assets/green.png","Green"),
    "blue": Button(100,100,1000,500,"assets/blue.png","Blue"),
}

def HomeButton(button, game):
    if game["oven_game"]:
        button.image_rect.x = 950
    elif game["toppings_time"]:
        button.image_rect.x = 300
    else:
        button.image_rect.x = 418
    button.draw(screen)

def HomeReturn(oven, returnhome, currentscreen, core, add, top,games,played,shop,bowl):
    currentscreen = False
    returnhome = True
    games["toppings_time"] = False
    played["oven_played"] = False
    oven = False
    bowl = None
    own = False
    own = exitclicked(games,shop, own)
    for name,item in core.items():
        item.achieved_value = 0
        if name == "butter":
            item.achieved_value = []
        item.added = False
    for name,item, in add.items():
        item.added = False
    for name,item, in top.items():
        item.added = False
    return returnhome, currentscreen, oven, played, bowl

def exitclicked(games,shop,own):
    for name,item in games.items():
        if name == "toppings_time" and games[name]:
            games[name] = True
        else:
            games[name] = False
    games["clicked_button"] = True
    shop.clicks = 0
    own = False
    return own

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
               "milk" : Core("assets/milk.png",1275,620,200)
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

def homescreen(levelbutton, shop, play, tut, games, miniimage, minirect, exit,leveldict,adds,tops,left,right,coins,coinstext):
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

    if games["show_shop"]:
        screen.blit(coinstext,(720,150))
        for name, add, in adds.items():
            if add.slide == shop.clicks:
                screen.blit(add.shop_img,add.shop_img_rect)
                if not add.owned:
                    screen.blit(add.buy_photo,add.buy_rect)
                    add.name = name
                    add.draw_description(name)
                    if add.try_purchase(event):
                        if coins>=add.cost:
                            coins -= add.cost
                            add.owned = True
                            coinstext = font.render(f"Balance: {coins}", True, "Black")
                if add.owned:
                    screen.blit(add.no_buy_photo,add.no_buy_rect)
        for name, top, in tops.items():
            if top.slide == shop.clicks and name not in adds:
                screen.blit(top.shop_img,top.shop_img_rect)
                if not top.owned:
                    screen.blit(top.buy_photo,top.buy_rect)
                    top.name = name
                    top.draw_description(name)
                    if top.try_purchase(event):
                        if coins>=top.cost:
                            coins -= top.cost
                            top.owned = True
                            coinstext = font.render(f"Balance: {coins}", True, "Black")
                if top.owned:
                    screen.blit(top.no_buy_photo,top.no_buy_rect)
        if shop.clicks > 0:
            left.draw(screen)

        if shop.clicks < 1:
            right.draw(screen)
    return coins,coinstext


def addlevel(leveldict,completed,adds,tops,core_list):
    if len(completed) <= len(leveldict) and len(leveldict) > 0:
        leveldict[len(completed)] = level(len(completed))
        Ingredients = {"order": Core(None,0,0), 
               "butter" : Core(None,342,2,[[randint(550,700),randint(400,500)],[randint(700,850),randint(400,500)], [randint(850,1050),randint(400,500)], [randint(800,1050),randint(500,600)], [randint(550,800),randint(500,600)]]),
               "eggs" : Core(None,810,0,randint(1,5)),
               "flour" : Core(None,1275,13,(690- randint(400,600)) * 3),
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

def level_clicking(button,event,games,leveldict,playing,current,play,tut):
    if button.is_clicked(event) and not games["show_minigame"]:
        games["show_levels"] = True
        games["show_minigame"] = True

    if play.is_clicked(event) and not games["show_minigame"]:
        current = leveldict[list(leveldict)[-1]]
        playing = True
        games["clicked_button"] = True
    
    if tut.is_clicked(event) and not games["show_minigame"]:
        current = leveldict["tutorial"]
        playing = True
        games["clicked_button"] = True

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

def shop_clicking(button,games,left, right):
    if button.is_clicked(event) and not games["show_minigame"]:
        games["show_shop"] = True
        games["show_minigame"] = True

    if left.is_clicked(event) and not games["clicked_button"]:
        games["clicked_button"] = True
        button.clicks -=1

    if right.is_clicked(event) and not games["clicked_button"]:
        games["clicked_button"] = True
        button.clicks +=1

    if left.is_clicked_up(event) or right.is_clicked_up(event):
        games["clicked_button"] = False


not_owned_text = font.render("Ingredient Not Owned. Buy in Shop", True, (0,0,0))
not_owned_mini = False

def addclicking(adds, games,own,color):
    for name, item in adds.items():
        if item.clicked(event): 
            if item.owned and not games["toppings_time"]:
                if name != "food coloring":
                    item.added = True
                    if name == "chocolate chips":
                        color = (123,63,0)
                    if name == "sprinkles":
                        color = (255,192,203)
                    if name == "oats":
                        color = (209,179,153)
                    if name == "peanuts":
                        color = (120, 47, 22)
                    if name == "pistachio":
                        color = (147, 197, 114)
                    if name == "matcha":
                        color = (145, 181, 0)
                    if name == "raisins":
                        color = (36, 33, 36)
                if name == "food coloring":
                    games["add_coloring"] = True
            if not item.owned and not games["toppings_time"]:
                own = True
    return own, color

def topclicking(tops,games,own):
    for name, item in tops.items():
        if item.clicked(event): 
            if item.owned:
                if name == "icing":
                    games["add_icing"] = True
                else:
                    item.added = True
            if not item.owned:
                own = True
    return own

def add_top_draw(adds,tops,games,own,text):
    if games["added_icing"] and not games["show_minigame"]:
        tops["icing"].added = True
    for name, item in adds.items():
        if name == "matcha" and item.added:
            g+=50
        if name != "food coloring" and name!= "matcha" and item.added and games["toppings_time"]:
            screen.blit(item.show_img, (0,0))
    for name, item in tops.items():
        if item.added:
            screen.blit(item.show_img, (0,0))
        if own:
            games["show_minigame"] = True
            screen.blit(text, (550,440))

def choosecolor(colors,games,adds,cookie):
    color_order = ["red", "green", "blue"]
    games["show_minigame"] = True
    for shade, button in colors.items():
        button.draw(screen)
        if button.is_clicked(event):
            adds["food coloring"].achieve_rgb = [0,0,0]
            adds["food coloring"].achieve_rgb[color_order.index(shade)] = 50
            adds["food coloring"].added = True
            cookie.fill(tuple(adds["food coloring"].achieve_rgb), special_flags=pygame.BLEND_RGB_ADD)

def chooseicing(colors,games,tops,exit):
    color_order = ["red", "green", "blue"]
    games["show_minigame"] = True
    for shade, button in colors.items():
        button.draw(screen)
        if button.is_clicked(event):
            tops["icing"].achieve_rgb = [50,50,50]
            tops["icing"].achieve_rgb[color_order.index(shade)] = 255
            tops["icing"].show_img.fill(tuple(tops["icing"].achieve_rgb), special_flags=pygame.BLEND_RGB_MIN)
            games["added_icing"] = True

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
egg_text = font.render(f"Eggs: {Core_Ingredient["eggs"].achieved_value}", True, (0,0,0))

#updates egg position as they fall and increments count when they fall in the basket
def egg_collisions(egg_list,left,right,bottom,top,length,core,fallen,games,played,text,color,r):
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
            fallen += 1
        if egg.rect.top >= length and not egg.fallen:
            egg.fallen = True
            fallen += 1
        
        if fallen == 5:
            color = (255, 210, 0)
            r += 10
            games["eggs_game"] = False
            played["eggs_played"] = True
            games["show_minigame"] = False

        screen.blit(text,(1100,150))
    return fallen, text,color,r

def basket_update(rect,bottom,left,right,top):
    bottom.update(rect.x, rect.y+rect.height-10, rect.width, 10)
    left.update(rect.x, rect.y, 10, rect.height)
    right.update(rect.x+rect.width-10, rect.y, 10, rect.height)
    top.update(rect.x+10, rect.y, rect.width-20, 10)

#checks if eggs are in basket
    
def eggcontrols(basket,basketrect,minirect,bottom,left,right,top,egglist):
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

milk_text = font.render(f"Volume: {Core_Ingredient["milk"].achieved_value}", True, "Black")

def milkclicking(can):
    if can.clicked(event):
        can.toggle_rotation()
        if not can.poured and can.turned:
            can.poured = True

def milk_game_controls(can,h,y,core,games,played,text,color,r):
    can.draw(screen)
    milk_cup = pygame.draw.rect(screen, "black", [700, 400, 300, 300], 10)
    milk_fill = pygame.draw.rect(screen, "white", [710, y, 280, h])
    
    if can.turned:
        milk_liquid = pygame.draw.rect(screen, "white", [840,213,10,477])
        h+=1
        y-=1
        core["milk"].achieved_value += 2
        text = font.render(f"Volume: {core["milk"].achieved_value}", True, "Black")

    if can.turned and core["milk"].achieved_value >= 560:
        can.toggle_rotation()
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    if not can.turned and can.poured:
        r += 10
        color = (253, 255, 246)
        games["milk_game"] = False
        played["milk_played"] = True
        games["show_minigame"] = False

    screen.blit(text, (1100,150))

    return h,y,text,color,r

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
flour_text = font.render(f"Volume: {int(Core_Ingredient["flour"].achieved_value/100)}", True, "Black")

def flourfalling(right,x,pour,h,flourx,flourw,rect,y,core,image,imagerect,complete,completerect,flour_volume_text):
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
            core["flour"].achieved_value += abs(cup.y - rect.y)
            flour_volume_text = font.render(f"Volume: {int(core["flour"].achieved_value/100)}", True, "Black")

    return x,h,y,right,flourx,flourw,flour_volume_text

def flourkeys(games,pour,played,color,r):
    flour_keys = pygame.key.get_pressed()
    if flour_keys[pygame.K_DOWN]:
        pour = True
    else: 
        pour = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if flour_complete_rect.collidepoint(mouse_pos):
            color = (245, 236, 226)
            r+= 10
            games["flour_game"] = False
            played["flour_played"] = True
            games["show_minigame"] = False
    return pour,color,r

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
Core_Ingredient["sugar"].achieved_value = [0,0]
sugar_text = font.render(f"Sugar Collected: {Core_Ingredient["sugar"].achieved_value[0]}", True, "Black")
salt_text = font.render(f"Salt Collected: {Core_Ingredient["sugar"].achieved_value[1]}", True, "Black")

def sugarcontrols(sugarlist,top,left,right,games,played,core,sugarstext,saltstext,color,r):
    for ingredient in sugarlist:
        ingredient.update()
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "sugar":        
            core["sugar"].achieved_value[0] += 1
            sugarlist.remove(ingredient)
            sugarstext = font.render(f"Sugar Collected: {core["sugar"].achieved_value[0]}", True, "Black")
        if ingredient.rect.colliderect(top) and ingredient.x >= left.x and ingredient.x <= right.x and ingredient.type == "salt":        
            sugarlist.remove(ingredient)
            core["sugar"].achieved_value[1] += 1
            saltstext = font.render(f"Salt Collected: {core["sugar"].achieved_value[1]}", True, "Black")
        if ingredient.rect.y >= 900:
            sugarlist.remove(ingredient)

    for ingredient in sugarlist:
        ingredient.draw(screen)
    screen.blit(basket, basket_rect)

    screen.blit(sugarstext,(950,150))
    screen.blit(saltstext,(950,200))

    if not sugarlist:
        color = (255, 255, 255)
        r+= 10
        games["sugar_game"] = False
        played["sugar_played"] = True
        games["show_minigame"] = False

    return sugarlist,sugarstext,saltstext,color,r

#butter game initialization

Core_Ingredient["butter"].achieved_value = []
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

def butterclicking(core,back,games,text):
    if len(core["butter"].achieved_value)<=4:
        mouse_pos = event.pos
        if back.collidepoint(mouse_pos) and not games["clicked_button"]:
            core["butter"].achieved_value.append(pygame.mouse.get_pos())

    text = font.render(f"Current volume: {int(shoelace(core["butter"].achieved_value)/1000)}", True, "black")
    return text

def butterdrawing(current,y,games,played,fallen,text,core,color):
    for i in range(5):
        pygame.draw.line(screen, "green", (current.core_ingredients["butter"].expected_value[i%5][0],current.core_ingredients["butter"].expected_value[i%5][1]),(current.core_ingredients["butter"].expected_value[(i+1)%5][0],current.core_ingredients["butter"].expected_value[(i+1)%5][1]),10)
    for i in range(len(core["butter"].achieved_value)):
        pygame.draw.circle(screen,"black",core["butter"].achieved_value[i],2)
        if len(core["butter"].achieved_value) >= 2:
            pygame.draw.line(screen, "black", core["butter"].achieved_value[i%(len(core["butter"].achieved_value))],core["butter"].achieved_value[(i+1)%len(core["butter"].achieved_value)],5)

    if len(core["butter"].achieved_value) == 5 and not fallen:
        fallen = [list(x) for x in core["butter"].achieved_value]

    if len(core["butter"].achieved_value) == 5:
        color = (255, 253, 116)
        pygame.draw.polygon(screen,(200,200,200),fallen)
        pygame.draw.polygon(screen,(255, 253, 116),core["butter"].achieved_value)
        for i in range(5):
            fallen[i][1] += 2
            current.core_ingredients["butter"].expected_value[i][1] += 2
        y += 2

    if butter_back.y >= 900:
        games["butter_game"] = False
        played["butter_played"] = True
        games["show_minigame"] = False

    screen.blit(text,(950,150))
    
    return y,fallen,color

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

def ovenclicking(games,played,startshow,start,playing):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

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

    return startshow,playing

def nextclicking(next_button, games, played, current, level_list, startshow,completed_list,add,top,core,bowl):
    if next_button.is_clicked(event) and not games["clicked_button"]and not games["show_shop"]:
        games["clicked_button"] = True
        if not played["oven_played"]:
                games["oven_game"] = True
                startshow = True
        elif played["oven_played"] and not games["toppings_time"]:
            games["toppings_time"] = True
            games["oven_game"] = False
        elif games["toppings_time"]:
            if not games["finished_screen"]:
                games["finished_screen"] = True
                return current,level_list,startshow,bowl
            completed_list[len(completed_list)] = current
            level_list = addlevel(level_list,completed_list,add,top,Core_Ingredient)
            current = level_list[len(completed_list)]
            games["toppings_time"] = False
            played["oven_played"] = False
            own = False
            own = exitclicked(games,shop_button, own)
            for name,item in core.items():
                item.achieved_value = 0
                if name == "butter":
                    item.achieved_value = []
                item.added = False
            for name,item in add.items():
                item.added = False
            for name,item in top.items():
                item.added = False
            return current,level_list,startshow,bowl
        bowl = None

    if next_button.is_clicked_up(event):
        games["clicked_button"] = False

    return current,level_list,startshow,bowl

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
         "finished_screen": False,
         "toppings_time": False,
         "add_coloring": False,
         "add_icing": False,
         "added_icing": False,
         "show_shop": False
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
running = True
#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #controls key in sugar game
        if Games["sugar_game"]:
            sugarkeys(basket_rect,basket,basket_bottom,basket_left,basket_right,basket_top)

        level_playing, current_level = level_clicking(level_button,event,Games,levels,level_playing,current_level,play_button,tutorial_button)
        shop_clicking(shop_button,Games,next_left, next_right)

        #control keys in flour game
        flour_pour,bowl_color,bowl_r = flourkeys(Games,flour_pour,Played,bowl_color,bowl_r)

        #If exit is pressed minigame disappears
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event):
                not_owned_mini = exitclicked(Games,shop_button, not_owned_mini)
            
            if home.is_clicked(event):
                show_home, level_playing, oven_game, Played, bowl_color = HomeReturn(oven, show_home, level_playing, Core_Ingredient, Add_Ins, Toppings,Games,Played,shop_button,bowl_color)

            if Games["toppings_time"]:
                not_owned_mini = topclicking(Toppings, Games,not_owned_mini)

            if Games["milk_game"]:
                milkclicking(milk_can)

            if Games["butter_game"]:
                butter_text = butterclicking(Core_Ingredient,butter_back,Games,butter_text)

            else:
                not_owned_mini, bowl_color = addclicking(Add_Ins, Games,not_owned_mini,bowl_color)

            #if ingredients have been clicked then minigame gets shown
            for name, item in Core_Ingredient.items():
                if item.clicked(event) and not Games["show_minigame"] and not Games["clicked_button"] and name != 'order':
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

        startbutton_show,oven_playing = ovenclicking(Games,Played,startbutton_show,startbutton_rect,oven_playing)

    if show_home:
        Money,balance_text = homescreen(level_button, shop_button, play_button, tutorial_button, Games, minigame, minigame_rect, exit_button,levels,Add_Ins,Toppings,next_left,next_right,Money,balance_text)

    if level_playing:
        screen.blit(background, (0,0))
        next.draw(screen)
        HomeButton(home, Games)
        for name, item in Core_Ingredient.items():
            item.draw(screen)

        if bowl_color:
            pygame.draw.circle(screen,bowl_color, (800,580), bowl_r)

        for name, item in Add_Ins.items():
            item.draw(screen)
            item.not_owned(screen)

        current_level.order.draw(screen)
        current_level,levels,startbutton_show,bowl_color = nextclicking(next, Games, Played, current_level, levels, startbutton_show,completed_levels,Add_Ins,Toppings,Core_Ingredient,bowl_color)

        if Games["show_minigame"]:
            screen.blit(minigame,minigame_rect)
            exit_button.draw(screen)

        if Games["order_open"]:
            order_texts = order_recipe(order_texts, current_level, screen, Games, exit_button) 

        #egg minigame
        if Games["eggs_game"]:
            eggcontrols(basket,basket_rect,minigame_rect,basket_bottom,basket_left,basket_right,basket_top,eggs)
            egg_fallen,egg_text,bowl_color,bowl_r = egg_collisions(eggs,basket_left,basket_right,basket_bottom,basket_top,height,Core_Ingredient,egg_fallen,Games,Played,egg_text,bowl_color,bowl_r)

        if Games["milk_game"]:
            milk_h,milk_y,milk_text,bowl_color,bowl_r = milk_game_controls(milk_can,milk_h,milk_y,Core_Ingredient,Games,Played,milk_text,bowl_color,bowl_r)

        if Games["flour_game"]:
            sieve_x,sieve_h,sieve_y,flour_right,flour_front_x,flour_front_w,flour_text = flourfalling(flour_right,sieve_x,flour_pour,sieve_h,flour_front_x,flour_front_w,sieve_rect,sieve_y,Core_Ingredient,sieve,sieve_rect,flour_complete,flour_complete_rect,flour_text)

        if Games["sugar_game"]:
            SugarSalts,sugar_text,salt_text,bowl_color,bowl_r = sugarcontrols(SugarSalts,basket_top,basket_left,basket_right,Games,Played,Core_Ingredient,sugar_text,salt_text,bowl_color,bowl_r)

        if Games["butter_game"]:
            butter_back = pygame.draw.rect(screen, (255, 253, 116), [width/2-250,butter_back_y,500,200,])
            butter_back_y,fallen_butter,bowl_color = butterdrawing(current_level,butter_back_y,Games,Played,fallen_butter,butter_text,Core_Ingredient,bowl_color)
        
        if Games["add_coloring"]:
            choosecolor(Color_Buttons,Games,Add_Ins,cookies)

        if Games["already_played"]:
            screen.blit(already_played_text, (680,440))

        if Games["oven_game"]:
            oven_r,oven_g,oven_b,oven_width= ovendraw(oven,oven_rect,oven_r,oven_g,oven_b,oven_width,startbutton_show,startbutton,startbutton_rect,stopbutton,stopbutton_rect,next,current_level)
            current_level,levels,startbutton_show,bowl_color = nextclicking(next, Games, Played, current_level, levels, startbutton_show,completed_levels,Add_Ins,Toppings,Core_Ingredient,bowl_color)
            HomeButton(home, Games)

        add_top_draw(Add_Ins,Toppings,Games,not_owned_mini,not_owned_text)

        if Games["toppings_time"]:
            screen.blit(traybackground, (0,0))
            screen.blit(cookies, (0,0))
            next.draw(screen)
            current_level.order.draw(screen)
            for name, item in Toppings.items():
                item.draw(screen)
                item.not_owned(screen)
            if Games["show_minigame"]:
                screen.blit(minigame,minigame_rect)
                exit_button.draw(screen)
            if Games["order_open"]:
                order_texts = order_recipe(order_texts, current_level, screen, Games, exit_button) 
            HomeButton(home, Games)
            add_top_draw(Add_Ins,Toppings,Games,not_owned_mini,not_owned_text)
            if Games["add_icing"]:
                chooseicing(Color_Buttons,Games,Toppings,exit_button)
            current_level,levels,startbutton_show,bowl_color = nextclicking(next, Games, Played, current_level, levels, startbutton_show,completed_levels,Add_Ins,Toppings,Core_Ingredient,bowl_color)
            if Games["finished_screen"]:
                screen.blit(minigame,minigame_rect)


    pygame.display.flip()
    clock.tick(fps)

pygame.quit