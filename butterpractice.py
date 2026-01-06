import pygame
from random import randint

clock = pygame.time.Clock()
fps = 60

pygame.init()

width = 1600
#550 - 1050
height = 900
#400 -600
screen = pygame.display.set_mode((width, height))

butter_expected_vertices = [[randint(550,700),randint(400,500)],[randint(700,850),randint(400,500)], [randint(850,1050),randint(400,500)], [randint(800,1050),randint(500,600)], [randint(550,800),randint(500,600)]]
butter_chosen_vertices = []
butter_back_y = height/2-50
fallen_butter = []

#shoelace formula
butter_expected_total = 0
for i in range(5):
    butter_xy = butter_expected_vertices[i%5][0]*butter_expected_vertices[(1+i)%5][1]
    butter_yx = butter_expected_vertices[i%5][1]*butter_expected_vertices[(1+i)%5][0]
    butter_expected_total += (butter_xy-butter_yx)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if len(butter_chosen_vertices)<=4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if butter_back.collidepoint(mouse_pos):
                    butter_chosen_vertices.append(pygame.mouse.get_pos())

        butter_chosen_total = 0
        for i in range(len(butter_chosen_vertices)):
            butter_xy = butter_chosen_vertices[i%len(butter_chosen_vertices)][0]*butter_chosen_vertices[(1+i)%len(butter_chosen_vertices)][1]
            butter_yx = butter_chosen_vertices[i%len(butter_chosen_vertices)][1]*butter_chosen_vertices[(1+i)%len(butter_chosen_vertices)][0]
            butter_chosen_total += (butter_xy-butter_yx)

    screen.fill((200,200,200))
    butter_back = pygame.draw.rect(screen, (255, 253, 116), [width/2-250,butter_back_y,500,200,])
    for i in range(5):
        pygame.draw.line(screen, "green", (butter_expected_vertices[i%5][0],butter_expected_vertices[i%5][1]),(butter_expected_vertices[(i+1)%5][0],butter_expected_vertices[(i+1)%5][1]),10)
    for i in range(len(butter_chosen_vertices)):
        pygame.draw.circle(screen,"black",butter_chosen_vertices[i],2)
        if len(butter_chosen_vertices) >= 2:
            pygame.draw.line(screen, "black", butter_chosen_vertices[i%(len(butter_chosen_vertices))],butter_chosen_vertices[(i+1)%len(butter_chosen_vertices)],5)

    if len(butter_chosen_vertices) == 5 and not fallen_butter:
        fallen_butter = [list(x) for x in butter_chosen_vertices]

    if len(butter_chosen_vertices) == 5:
        pygame.draw.polygon(screen,(200,200,200),fallen_butter)
        pygame.draw.polygon(screen,(255, 253, 116),butter_chosen_vertices)
        for i in range(5):
            fallen_butter[i][1] += 2
            butter_expected_vertices[i][1] += 2
        butter_back_y += 2
        


    pygame.display.flip()
    clock.tick(fps)

pygame.quit()