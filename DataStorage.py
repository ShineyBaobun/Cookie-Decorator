import pickle
from HomeScreen import level,Core,Topping

def Store_Data(levels,money):
    """
    Stores necessary data into the datastorage.pkl file so it can be accessed again later
    
    :param levels: dictionary of levels
    :param money: player's earned money
    """
    data = {"Money": money,
            "n": [],
            "expected_core": [],
            "stars": [],
            "adds": [],
            "tops": [],
            "addcolor": [],
            "topcolor": []}
    
    for num,lev in levels.items():
        add_names = []
        add_colors = []
        top_names = []
        top_colors = []
        core_values = []
        for name,item in lev.core_ingredients.items():
            core_values.append(item.expected_value)
        for name, item in lev.add_ins.items():
            add_names.append(name)
            add_colors.append(item.color)
        for name, item in lev.toppings.items():
            top_names.append(name)
            top_colors.append(item.color)
        data["expected_core"].append(core_values)
        data["adds"].append(add_names)
        data["tops"].append(top_names)
        data["addcolor"].append(add_colors)
        data["topcolor"].append(top_colors)
        data["n"].append(lev.n)
        data["stars"].append(lev.stars)

    pickle.dump(data, open('datastorage.pkl','wb'))

def Load_Data(level_list,money,buttons,event,mini_image,screen,loaded_bool):
    """
    Loads the data that has been stored in datastorage.pkl so a previous game can be accessed by the user
    
    :param level_list: dictionary of levels
    :param money: user's money
    :param buttons: dictionary of buttons
    :param event: tracks the events carries out by the user
    :param mini_image: image of the minigame background
    :param screen: the surface that images appear on
    :param loaded_bool: boolean list that identifies whether a game has been loaded
    """
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
    
    Colors = ["red", "green", "blue"]
    
    screen.fill((225, 150, 164))
    screen.blit(mini_image,(256,109))
    buttons["NewGame"].draw(screen)
    buttons["StoredGame"].draw(screen)
    if buttons["NewGame"].is_clicked(event):
        loaded_bool = True
        return money,loaded_bool
    if buttons["StoredGame"].is_clicked(event):
        loaded = pickle.load(open('datastorage.pkl', 'rb'))
        for n in loaded['n']:
            level_list[n] = level(n)
            level_list[n].core_ingredients = {"butter" : Core(None,342,2,loaded["expected_core"][n][0]),
                                              "eggs" : Core(None,810,0,loaded["expected_core"][n][1]),
                                              "flour" : Core(None,1275,13,loaded["expected_core"][n][2]),
                                              "sugar" : Core(None,1275,320,loaded["expected_core"][n][3]),
                                              "milk" : Core(None,1275,620,loaded["expected_core"][n][4])}
        for x, (list) in enumerate(loaded["adds"]):
            for i, (name) in enumerate(list):
                level_list[x].add_ins[name] = Adds[name]
                if loaded["addcolor"][x][i] in Colors:
                    level_list[x].add_ins[name].expect_rgb = [0,0,0]
                    level_list[x].add_ins[name].expect_rgb[Colors.index(loaded["addcolor"][x][i])] = 100
                    level_list[x].add_ins[name].color = loaded["addcolor"][x][i]

        for x, (list) in enumerate(loaded["tops"]):
            level_list[x].stars = loaded["stars"][x]
            for i, (name) in enumerate(list):
                level_list[x].toppings[name] = Tops[name]
                if loaded["topcolor"][x][i] in Colors:
                    level_list[x].toppings[name].expect_rgb = [50,50,50]
                    level_list[x].toppings[name].expect_rgb[Colors.index(loaded["topcolor"][x][i])] = 255
                    level_list[x].toppings[name].color = loaded["topcolor"][x][i]

        loaded_bool = True
        money = loaded["Money"]
        
    return money,loaded_bool

