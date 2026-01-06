import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900
screen = pygame.display.set_mode((width, height))

sieve = pygame.image.load("assets/sieve.png")
sieve = pygame.transform.scale(sieve, (300,150))
sieve_rect = sieve.get_rect(center=(width/2,height/2-200))
right = True
sieve_y = 690
sieve_x = 600
sieve_h = 0
flour_front_w = 150
flour_front_x = sieve_rect.x + 75

running = True
flour_pour = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        flour_keys = pygame.key.get_pressed()
        if flour_keys[pygame.K_DOWN]:
            flour_pour = True
        else: 
            flour_pour = False

    screen.fill("pink")
    screen.blit(sieve,sieve_rect)
    Cup = pygame.draw.rect(screen, "black", [sieve_x, 500, 300, 200], 10)
    fill = pygame.draw.rect(screen, "white", [sieve_x+10, sieve_y, 280, sieve_h])
    
    if right:
        sieve_x += 7
    else:
        sieve_x -= 7
    if sieve_x >= 1000:
        right = False
    if sieve_x <= 300:
        right = True


    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        flour_pour = True

    if flour_pour and sieve_h < 190:
        flourfront = pygame.draw.rect(screen, "white", [flour_front_x,sieve_rect.y + 150,flour_front_w,800])
        flourback = pygame.draw.rect(screen, "white", [sieve_rect.x + 75,sieve_rect.y + 150,150, Cup.y - sieve_rect.y + 40])
        if Cup.x <= flourback.x + 150 and Cup.x +300 >= flourback.x:
            sieve_h+=1
            sieve_y-=1
            if Cup.x > sieve_rect.x and Cup.x < sieve_rect.x + 225:
                flour_front_w = Cup.x - sieve_rect.x - 75
                flour_front_x = sieve_rect.x + 75
            elif Cup.x < sieve_rect.x and Cup.x +300 > sieve_rect.x + 75:
                flour_front_w = sieve_rect.x -75 - Cup.x
                flour_front_x = Cup.x + 300
            else:
                flour_front_w = 150
                flour_front_x = sieve_rect.x + 75
    


    pygame.display.flip()
    clock.tick(fps)

pygame.quit()