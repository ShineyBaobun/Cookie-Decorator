import pygame

pygame.init()

width = 1600
height = 900

x=0
y=0

screen = pygame.display.set_mode((width, height))

plain = pygame.image.load('assets/cookie.webp')
plain.fill((75, 0, 110, 0), special_flags=pygame.BLEND_RGBA_ADD)
sprinkles = pygame.image.load('assets/sprinkles.webp')

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            plain_rect = plain.get_rect(topleft = (x,y))
            if plain_rect.collidepoint(mouse_pos):
                x += 5

    screen.fill((255,255,255))
    mouse = pygame.mouse.get_pos()

    screen.blit(plain, (x,y))
    screen.blit(sprinkles, (x,y))

    pygame.display.flip()