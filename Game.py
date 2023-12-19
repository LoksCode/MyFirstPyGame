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
ground_rect = ground_surface.get_rect(midbottom=(800, 100))

score_surface = pixel_font.render('my game', False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(400, 50))

blob_surface = pygame.image.load('graphics/blob1.png').convert_alpha()
blob_surface = pygame.transform.scale(blob_surface, (80, 40))
blob_rect = blob_surface.get_rect(midbottom=(800, 300))

player_surface = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (60, 80))
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0


# Main game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                player_gravity = -20

    screen.blit(sky_surface, (0, 0))  # draw the background
    screen.blit(ground_surface, (0, 300))  # draw the floor
    pygame.draw.rect(screen, '#17a62d', score_rect)           # draw the score rectangle
    pygame.draw.rect(screen, '#17a62d', score_rect.inflate(10, 10))  # draw the score rectangle outline

    screen.blit(score_surface, score_rect)  # draw the score
    # blob
    blob_rect.left -= 4
    screen.blit(blob_surface, blob_rect)
    if blob_rect.right <= 0:
        blob_rect.left = 800

    # player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300

    screen.blit(player_surface, player_rect)  # draw the player

    pygame.display.update()
    clock.tick(60)  # set frame rate
