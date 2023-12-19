import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Sprinter')
clock = pygame.time.Clock()

# importing and converting graphics
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

text_surface = pixel_font.render('Sprinter', False, 'black')
text_rect = text_surface.get_rect(midbottom=(400, 50))

blob_surface = pygame.image.load('graphics/blob1.png').convert_alpha()
blob_surface = pygame.transform.scale(blob_surface, (80, 40))
blob_rect = blob_surface.get_rect(midbottom=(800, 300))

player_surface = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (60, 80))
player_rect = player_surface.get_rect(midbottom=(80, 300))

# Main game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))  # draw the background
    screen.blit(ground_surface, (0, 300))  # draw the floor
    screen.blit(text_surface, text_rect)  # draw the score
    screen.blit(player_surface, player_rect)  # draw the player

                                                 #blob moving
    blob_rect.left -= 3
    screen.blit(blob_surface, blob_rect)
    if blob_rect.right <= 0:
        blob_rect.left = 800

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print("COLLISION")   ||| collision check with mouse and player hitbox


    pygame.display.update()
    clock.tick(60)  # set frame rate
