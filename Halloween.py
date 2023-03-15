""""
License: (CC0 1.0 Universal) You're free to use these game assets in any project, personal or commercial.
There's no need to ask permission before using these. Giving attribution is not required, but is greatly appreciated!
This is for the Graveyard kit from kenney.nl.
"""

import pygame
import random
import time

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_f,
)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000


class Pumpkin(pygame.sprite.Sprite):
    def __init__(self):
        super(Pumpkin, self).__init__()
        image = pygame.image.load("pumpkin.png").convert()

        image = pygame.transform.scale(image, (171,152))
        self.surf = image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemies, self).__init__()
        enemy_img = pygame.image.load("reaper1.png").convert()
        self.surf = enemy_img
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH - 1, SCREEN_WIDTH + 1),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Lazer(pygame.sprite.Sprite):
    def __init__(self, pumpkin):
        super(Lazer, self).__init__()
        self.surf = pygame.Surface((100, 10))
        orange = (255, 165, 0)
        self.surf.fill(orange)
        self.rect = self.surf.get_rect(center=pumpkin.rect.center)
        self.update()

    def update(self):
        self.rect.move_ip(5, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("Halloween")

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)

pumpkin = Pumpkin()
lazers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(pumpkin)

pygame.mixer.music.load("Halloween .wav")
pygame.mixer.music.play(loops=-1)

game_over_sound = pygame.mixer.Sound("ThisGameIsOver.wav")
collision_sound = pygame.mixer.Sound("spell3.wav")
enemy_hit_sound = pygame.mixer.Sound("Large Monster Death 02.wav")

score = 0
score_font = pygame.font.Font(None, 24)

lives = 3
life_font = pygame.font.Font(None, 24)
running = True
damage_start = None

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if event.type == ADDENEMY:
            new_enemy = Enemies()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == KEYDOWN:
            if event.key == K_f:
                new_lazer = Lazer(pumpkin)
                lazers.add(new_lazer)
                all_sprites.add(new_lazer)

    screen.fill((0, 0, 0))

    pressedkeys = pygame.key.get_pressed()

    pumpkin.update(pressedkeys)
    enemies.update()
    lazers.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    score_text = score_font.render(f"Current score: {score}", (255, 255, 255), (255, 165, 0))
    score_rect = score_text.get_rect()
    score_rect.top = 0
    score_rect.left = 0
    screen.blit(score_text, score_rect)

    life_text = life_font.render(f"Lives: {lives}", (255, 255, 255), (255, 165, 0))
    life_rect = life_text.get_rect()
    life_rect.right = SCREEN_WIDTH
    life_rect.top = 0
    screen.blit(life_text, life_rect)

    for lazer_x in lazers:
        if pygame.sprite.spritecollide(lazer_x, enemies, dokill=True):
            print("[+] lazer hit enemy!")
            score += 1
            enemy_hit_sound.play()


    # set 3 second rule to only look for collisions 3 seconds after the last collision
    if damage_start:
        if int((time.time() - damage_start)) < 2 and lives > 0:
            # do not assess collisions/damage
            collision_sound.play()
        else:
            pumpkin_damage = pygame.sprite.spritecollide(pumpkin, enemies, dokill=False)
            print("[+] pumpkin_damage length = ", len(pumpkin_damage))
            print("[+] pumpkin_damage type = ", type(pumpkin_damage))
            print("[+] pumpkin_damage = ", pumpkin_damage)

    else:
        pumpkin_damage = pygame.sprite.spritecollide(pumpkin, enemies, dokill=False)
        print("[+] pumpkin_damage length = ", len(pumpkin_damage))
        print("[+] pumpkin_damage type = ", type(pumpkin_damage))
        print("[+] pumpkin_damage = ", pumpkin_damage)

    if pumpkin_damage:
        damage_start = time.time()
        lives -= len(pumpkin_damage)
        pumpkin_damage = 0

        if lives <= 0:
            pygame.mixer.music.stop()
            collision_sound.stop()
            pumpkin.kill()
            print("[-] You died.")
            game_over_sound.play()

    pygame.time.Clock().tick(180)

    pygame.display.flip()






