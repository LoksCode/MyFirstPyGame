import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
        player_walk1 = pygame.transform.scale(player_walk1, (60, 80))
        player_walk2 = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
        player_walk2 = pygame.transform.scale(player_walk2, (60, 80))
        self.player_jump = pygame.image.load('graphics/player_jump_1.png').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (65, 80))

        self.player_walk = [player_walk1, player_walk2]
        self.gravity = 0
        self.player_index = 0
        self.player_surf = self.player_walk[self.player_index]
        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(midbottom=(80, 300))

        self.jump_sound = pygame.mixer.Sound('sounds/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def position_restart(self):
        if not game_active:
            self.rect.bottom = 300
            self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.position_restart()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type =='fly':
            fly_frame1 = pygame.image.load('graphics/fly1.png').convert_alpha()
            fly_frame1 = pygame.transform.scale(fly_frame1, (70, 30))
            fly_frame2 = pygame.image.load('graphics/fly2.png').convert_alpha()
            fly_frame2 = pygame.transform.scale(fly_frame2, (70, 30))
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            blob_frame1 = pygame.image.load('graphics/blob1.png').convert_alpha()
            blob_frame1 = pygame.transform.scale(blob_frame1, (70, 30))
            blob_frame2 = pygame.image.load('graphics/blob2.png').convert_alpha()
            blob_frame2 = pygame.transform.scale(blob_frame2, (70, 30))
            self.frames = [blob_frame1, blob_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.erase()

    def erase(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    game_time = pygame.time.get_ticks() - start_time
    score_surface = pixel_font.render(f'Score: {round(game_time/1000)}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return game_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        game_over_music.play(loops=-1)
        game_music.stop()
        hit_sound.play()
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Sprinter')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
player_gravity = 0

#audio zone

game_music = pygame.mixer.Sound('sounds/gameost.wav')
game_music.set_volume(0.05)
menu_music = pygame.mixer.Sound('sounds/titleost.wav')
menu_music.play(loops=-1)
menu_music.set_volume(0.04)
game_over_music = pygame.mixer.Sound('sounds/pointsost.wav')
game_over_music.set_volume(0.05)
hit_sound = pygame.mixer.Sound('sounds/oor.mp3')


#groups
player = pygame.sprite.GroupSingle(Player())
player.add(Player())
obstacle_group = pygame.sprite.Group()

# importing and converting graphics
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(midbottom=(800, 100))

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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'blob', 'blob',])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                menu_music.stop()
                game_over_music.stop()
                game_music.play(loops=-1)
                game_active = 1

    if game_active:
        screen.blit(sky_surface, (0, 0))  # draw the background
        screen.blit(ground_surface, (0, 300))  # draw the floor
        score = display_score()  # Score takes the function value
        player.draw(screen)  #Player class is drawn
        obstacle_group.draw(screen)  #enemies class is drawn
        obstacle_group.update()  #enemies class is updated
        #collision function
        game_active = collision_sprite()

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

    player.update()
    pygame.display.update()
    clock.tick(60)  # set frame rate
