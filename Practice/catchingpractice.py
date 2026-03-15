import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900

basket = pygame.image.load('assets/basket.png')
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

screen = pygame.display.set_mode((width, height))

class egg:
    def __init__(self, w, h):
        self.x = randint(300,1250)
        self.y = randint(-250,-50)
        self.w = w
        self.h = h
        self.original_image = pygame.image.load('assets/egg.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (w,h))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.detect = False
        self.y_velocity = randint(2,4)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.y_velocity


eggs = [egg(50,75) for i in range(5)]
    
h = 10
y = 790
egg_count = 0

running = True

def CheckEgg(current, left, right, bottom):
    if current.rect.colliderect(left):
        return True
    if current.rect.colliderect(right):        
        return True
    if current.rect.colliderect(bottom):        
        return True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_rect.x > 0:
        basket_rect.x -= 5
    if keys[pygame.K_RIGHT] and basket_rect.x < width - basket_rect.width:
        basket_rect.x += 5
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
    
    for egg in eggs:
        egg.update() 
        if egg.rect.colliderect(basket_left) and egg.rect.x > basket_left.x:
            egg.rect.x = basket_left.x + 10
        if egg.rect.colliderect(basket_left) and egg.rect.x <= basket_left.x:
            egg.rect.x = basket_left.x-50
        if egg.rect.colliderect(basket_right) and egg.rect.x < basket_right.x:
            egg.rect.x = basket_right.x -50
        if egg.rect.colliderect(basket_right) and egg.rect.x >= basket_right.x+10:
            egg.rect.x = basket_right.x + 10
        if egg.rect.colliderect(basket_bottom):        
            egg.rect.y = basket_bottom.y -75
        if egg.rect.colliderect(basket_top):        
            egg_count += 1

    
    screen.fill((200,200,200))
    screen.blit(basket, basket_rect)
    for egg in eggs:
        egg.draw(screen)
        

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
