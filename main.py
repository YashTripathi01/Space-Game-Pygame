from constants import *

import pygame
import os
import sys

pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Fight')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# loading assets
GREY_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'grey_ship.png'))
WHITE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'white_ship.png'))
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'images', 'bg_1.jpg')), (WIDTH, HEIGHT))

# resizing and rotating the ship image
GREY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    GREY_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)
WHITE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    WHITE_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)

# loading sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('assets', 'sound', 'Grenade_1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('assets', 'sound', 'Gun_Silencer.mp3'))

# to divide the screen into two equal parts
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# custom event for collison
GREY_HIT = pygame.USEREVENT+1
WHITE_HIT = pygame.USEREVENT+2

# grey ship movement
def grey_movement(keys_pressed, grey):
    if keys_pressed[pygame.K_a] and grey.x - VEL > 0:  # LEFT
        grey.x -= VEL
    if keys_pressed[pygame.K_d] and grey.x + VEL + grey.width < BORDER.x:  # RIGHT
        grey.x += VEL
    if keys_pressed[pygame.K_w] and grey.y - VEL > 0:  # UP
        grey.y -= VEL
    if keys_pressed[pygame.K_s] and grey.y + VEL + grey.height < HEIGHT - 10:  # DOWN
        grey.y += VEL


# white ship movement
def white_movement(keys_pressed, white):
    if keys_pressed[pygame.K_LEFT] and white.x - VEL > BORDER.x + BORDER.width:  # LEFT
        white.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and white.x + VEL + white.width < WIDTH:  # RIGHT
        white.x += VEL
    if keys_pressed[pygame.K_UP] and white.y - VEL > 0:  # UP
        white.y -= VEL
    if keys_pressed[pygame.K_DOWN] and white.y + VEL + white.height < HEIGHT - 10:  # DOWN
        white.y += VEL


# to move bullets, handle collision of bullets and removing bullets when off the screen or collides with a character
def handle_bullets(grey_bullets, white_bullets, grey, white):
    # to check if the grey ships bullet hits the white ship
    for bullet in grey_bullets:
        bullet.x += BULLET_VEL
        # to check for collision - colliderect()
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))
            grey_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            grey_bullets.remove(bullet)

    # to check if the white ships bullet hits the grey ship
    for bullet in white_bullets:
        bullet.x -= BULLET_VEL
        # to check for collision - colliderect()
        if grey.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREY_HIT))
            white_bullets.remove(bullet)
        elif bullet.x < 0:
            white_bullets.remove(bullet)


# to draw on the window
def draw_window(grey, white, grey_bullets, white_bullets, grey_health, white_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    grey_health_text = HEALTH_FONT.render(
        'Health: ' + str(grey_health), 1, WHITE)
    white_health_text = HEALTH_FONT.render(
        'Health: ' + str(white_health), 1, WHITE)

    WIN.blit(grey_health_text, (10, 10))
    WIN.blit(white_health_text, (WIDTH-white_health_text.get_width()-10, 10))
    WIN.blit(GREY_SPACESHIP, (grey.x, grey.y))
    WIN.blit(WHITE_SPACESHIP, (white.x, white.y))

    for bullet in grey_bullets:
        pygame.draw.rect(WIN, GREY, bullet)

    for bullet in white_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


# display winning text
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


# main game loop
def main():
    grey = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    white = pygame.Rect(1000, 300, SHIP_WIDTH, SHIP_HEIGHT)

    # to store bullets of the ships
    grey_bullets = []
    white_bullets = []

    # health of ships
    grey_health = 10
    white_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(grey_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        grey.x + grey.width, grey.y + grey.height//2-2, BULLET_WIDTH, BULLET_HEIGHT)
                    grey_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(white_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        white.x, white.y + white.height//2-2, BULLET_WIDTH, BULLET_HEIGHT)
                    white_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GREY_HIT:
                grey_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == WHITE_HIT:
                white_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if grey_health <= 0:
            winner_text = 'White Wins!'

        if white_health <= 0:
            winner_text = 'Grey Wins!'

        if winner_text != '':
            draw_winner(winner_text)  # someone won
            break

        # to get info of what keys are currently being pressed
        keys_pressed = pygame.key.get_pressed()
        
        # function calls
        grey_movement(keys_pressed, grey)
        white_movement(keys_pressed, white)
        handle_bullets(grey_bullets, white_bullets, grey, white)
        draw_window(grey, white, grey_bullets,
                    white_bullets, grey_health, white_health)

    main()


if __name__ == '__main__':
    main()
