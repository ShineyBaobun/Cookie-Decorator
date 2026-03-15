import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900
screen = pygame.display.set_mode((width, height))

class SugarSalt:
    def __init__(self, y, type, x):
        self.x = x
        self.y = y
        self.type = type
        if self.type == "sugar":
            self.original_image = pygame.image.load('assets/sugarimage.webp').convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (75,75))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.type == "salt":
            self.original_image = pygame.image.load('assets/salt.jpg').convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (75,100))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 2

basket = pygame.image.load('assets/basket.png')
basket = pygame.transform.scale(basket, (250,150))
basket_rect = basket.get_rect()
basket_rect.topleft = (width/2-(basket.get_width()/2),500)

SugarSalts = []
sugar_collected = 0
salt_collected = 0

for i in range(5):
    nums = [375,width/2-37,1150]
    print(nums)
    chosen_x = nums[randint(0,2)]
    SugarSalts.append(SugarSalt(-50-(i*200),"sugar",chosen_x))
    nums.remove(chosen_x)
    chosen_x = nums[randint(0,1)]
    print(nums)
    SugarSalts.append(SugarSalt(-50-(i*200),"salt", chosen_x))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        sugar_keys = pygame.key.get_pressed()
        if sugar_keys[pygame.K_LEFT] and basket_rect.x != width/2-(basket.get_width()/2)-400:
            basket_rect.x -= 400
        if sugar_keys[pygame.K_RIGHT] and basket_rect.x != width/2-(basket.get_width()/2)+400:
            basket_rect.x += 400
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

    for thing in SugarSalts:
        thing.update()
        if thing.rect.colliderect(basket_top) and thing.x >= basket_left.x and thing.x <= basket_right.x and thing.type == "sugar":        
            sugar_collected += 1
            SugarSalts.remove(thing)
        if thing.rect.colliderect(basket_top) and thing.x >= basket_left.x and thing.x <= basket_right.x and thing.type == "salt":        
            SugarSalts.remove(thing)
            


    screen.fill((200,200,200))
    for thing in SugarSalts:
        thing.draw(screen)
    screen.blit(basket, basket_rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
