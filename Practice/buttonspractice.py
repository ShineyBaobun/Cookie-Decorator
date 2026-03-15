import pygame

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))

class Bottle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.original_image = pygame.image.load('assets/milk.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (w,h))
        self.rect = self.image.get_rect(center=(width/2, height/2))
        self.turned = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def toggle_rotation(self):
        self.turned = not self.turned
        angle = 45 if self.turned else -45
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

Water = Bottle(400, 100, 200, 200)
h = 0
y = 790

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Water.clicked(event):
            Water.toggle_rotation()

    screen.fill((250, 150, 150))
    Water.draw(screen)
    Cup = pygame.draw.rect(screen, "black", [200, 600, 300, 200], 10)
    fill = pygame.draw.rect(screen, "white", [210, y, 280, h])

    if Water.turned:
        liquid = pygame.draw.rect(screen, "white", [360,200,10,600-10])
        h+=1
        y-=1
    

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
