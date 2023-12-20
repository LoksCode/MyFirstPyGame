import pygame
from sys import exit


def display_score():
    game_time = pygame.time.get_ticks() - start_time
    score_surface = pixel_font.render(f'Score: {round(game_time/1000)}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return game_time

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Sprinter')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# importing and converting graphics
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/sky.png').convert()

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(midbottom=(800, 100))

blob_surface = pygame.image.load('graphics/blob1.png').convert_alpha()
blob_surface = pygame.transform.scale(blob_surface, (70, 30))
blob_rect = blob_surface.get_rect(midbottom=(800, 300))

player_surface = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (60, 80))
player_rect = player_surface.get_rect(midbottom=(80, 300))

# INTRO SCREEN
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (120, 140))
player_stand_rect = player_stand.get_rect(center=(400, 200))
welcome_message = pixel_font.render('The Sprinter Game', False, (95, 69, 74))
welcome_rect = welcome_message.get_rect(midbottom=(400, 100))

instruction = pixel_font.render('Press Spacebar to start', False, (95, 69, 74))
instruction_rect = instruction.get_rect(midbottom=(400, 330))


player_gravity = 0

#TIMERS
obstacle_timer = pygame.USEREVENT + 1


# Main game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                blob_rect.left = 800
                start_time = pygame.time.get_ticks()
                game_active = 1


    if game_active:
        screen.blit(sky_surface, (0, 0))  # draw the background
        screen.blit(ground_surface, (0, 300))  # draw the floor

        score = display_score()  # Score takes the function value


        # blob
        blob_rect.left -= 5
        screen.blit(blob_surface, blob_rect)
        if blob_rect.right <= 0:
            blob_rect.left = 800

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)  # draw the player

        # Collisions
        if blob_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((230, 93, 223))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(instruction, instruction_rect)
        if score <= 0:
            screen.blit(welcome_message, welcome_rect)
        else:
            score_surface2 = pixel_font.render(f'Your score:  {round(score/1000)}  points!', False, (64, 64, 64))
            score_rect2 = score_surface2.get_rect(midbottom=(400, 100))
            screen.blit(score_surface2, score_rect2)

    pygame.display.update()
    clock.tick(60)  # set frame rate
