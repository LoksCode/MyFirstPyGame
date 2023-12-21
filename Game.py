import pygame
from sys import exit
from random import randint


def display_score():
    game_time = pygame.time.get_ticks() - start_time
    score_surface = pixel_font.render(f'Score: {round(game_time/1000)}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return game_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 9
            if obstacle_rect.y <= 200: screen.blit(fly_surface, obstacle_rect)
            else: screen.blit(blob_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True



pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Sprinter')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
player_gravity = 0

# importing and converting graphics
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/sky.png').convert()

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(midbottom=(800, 100))

#enemies / obstacles

#blob
blob_surface = pygame.image.load('graphics/blob1.png').convert_alpha()
blob_surface = pygame.transform.scale(blob_surface, (70, 30))

#fly
fly_surface = pygame.image.load('graphics/fly1.png').convert_alpha()
fly_surface = pygame.transform.scale(fly_surface, (70, 30))

obstacle_rect_list = []

#PLAYER
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




#TIMERS
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

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
                start_time = pygame.time.get_ticks()
                game_active = 1

        if event.type == obstacle_timer and game_active:
            if randint(0, 1):
                obstacle_rect_list.append(blob_surface.get_rect(bottomright=(randint(900, 1000), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1000), 200)))

    if game_active:
        screen.blit(sky_surface, (0, 0))  # draw the background
        screen.blit(ground_surface, (0, 300))  # draw the floor
        score = display_score()  # Score takes the function value

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)  # draw the player

        # enemies movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((230, 93, 223))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(instruction, instruction_rect)
        obstacle_rect_list = []
        player_rect.midbottom = (80, 300)
        player_gravity = 0


        if score <= 0:
            screen.blit(welcome_message, welcome_rect)
        else:
            score_surface2 = pixel_font.render(f'Your score:  {round(score/1000)}  points!', False, (64, 64, 64))
            score_rect2 = score_surface2.get_rect(midbottom=(400, 100))
            screen.blit(score_surface2, score_rect2)

    pygame.display.update()
    clock.tick(60)  # set frame rate
