import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Sprinter')
clock = pygame.time.Clock()
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)


sky_surface = pygame.image.load('graphics/sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = pixel_font.render('Sprinter', False, 'black')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))  # draw the background
    screen.blit(ground_surface, (0, 300))  # draw the floor
    screen.blit(text_surface, (300, 50))  # draw the score
    pygame.display.update()
    clock.tick(60)  # set frame rate
