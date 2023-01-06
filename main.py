# if ur trying to understand the code, jump down to the main event loop and start from there

import random
from time import sleep
import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 900

# create window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PONG')

# create the ball, left right_player, and right right_player
ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
# right
right_player = pygame.Rect(screen_width - 40, screen_height/2 - 60, 30, 140)
# left
left_player = pygame.Rect(10, screen_height/2 - 60, 30, 140)

# how fast the players move
player_move_speed = 10

# how fast ball moves
ball_speed_x = 7
ball_speed_y = 7
ball_control_speed = player_move_speed / 2

# keep score
left_player_score = 0
right_player_score = 0

# used to make ball move in a random direction
first = True

font = pygame.font.SysFont("arial", 27)


def display_score():
    score = font.render(
        f"{left_player_score} :SCORE     SCORE: {right_player_score}", False, "white")

    # place the score text on the screen at the middle
    screen.blit(score, (500, 50))


# reset_positions ball, right_player, and left_player positions and get ready to make ball go in random direction
def reset_positions():
    ball.midbottom = (screen_width/2-15, screen_height/2-15)
    right_player.left = screen_width - 40
    right_player.top = screen_height/2 - 60

    left_player.left = 10
    left_player.top = screen_height/2 - 60
    global first
    first = True


# launches nukes to russia and china
def draw_ball():
    pygame.draw.ellipse(screen, "white", ball)


# draw players and center line
def draw_players():
    pygame.draw.rect(screen, "white", right_player)
    pygame.draw.rect(screen, "white", left_player)
    pygame.draw.aaline(screen, "white", (screen_width/2, 0),
                       (screen_width/2, screen_height))


# get the keys being pressed right now
def handle_keys():
    global hit_left, hit_right, ball_speed_y
    keys = pygame.key.get_pressed()
    if hit_right == False and hit_left == True:
        # sleep(10000000)
        ball_speed_y = 0
        if keys[pygame.K_w]:
            if ball.top >= 0:
                ball.centery -= ball_control_speed
        if keys[pygame.K_s]:
            if ball.bottom <= screen_height:
                ball.centery += ball_control_speed
        if keys[pygame.K_DOWN]:
            right_player.centery += player_move_speed
        if keys[pygame.K_UP]:
            right_player.centery -= player_move_speed
    elif hit_right == True and hit_left == False:
        if keys[pygame.K_w]:
            left_player.centery -= player_move_speed
        if keys[pygame.K_s]:
            left_player.centery += player_move_speed
        if keys[pygame.K_DOWN]:
            if ball.bottom <= screen_height:
                ball.centery += ball_control_speed
        if keys[pygame.K_UP]:
            if ball.top >= 0:
                ball.centery -= ball_control_speed
    else:
        if keys[pygame.K_w]:
            left_player.centery -= player_move_speed
        if keys[pygame.K_s]:
            left_player.centery += player_move_speed
        if keys[pygame.K_DOWN]:
            right_player.centery += player_move_speed
        if keys[pygame.K_UP]:
            right_player.centery -= player_move_speed


def randomize_ball_direction():
    global first, ball_speed_x, ball_speed_y
    # if a random number from 0, 10 is bigger than five, move left, else move right
    if random.randint(0, 10) >= 5:
        ball_speed_x *= -1
        ball_speed_y *= -1
    else:
        # dont need to change the speeds cause already positive
        first = False


def handle_player_points():
    global right_player_score, left_player_score
    # if ball goes past left players paddle:
    if ball.left <= 0:
        right_player_score += 1
        reset_positions()
        draw_ball()
    # if the ball goes past right players paddle
    if ball.right >= screen_width:
        left_player_score += 1
        reset_positions()
        draw_ball()


def handle_ball_bouncing():
    global ball_speed_x, ball_speed_y, hit_left, hit_right
    # bounce off the bottom and top walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1  # if it was headed down, now its headed up and vice versa

    # if it collides with a paddle, move in the opposite direction
    if ball.colliderect(right_player):
        ball_speed_x *= -1
        hit_left = False
        hit_right = True
    if ball.colliderect(left_player):
        ball_speed_x *= -1
        hit_right = False
        hit_left = True
    # print(
    #    f"has left hit the ball: {hit_left}, has right hit the ball: {hit_right}")


def handle_player_boundaries():
    # dont allow players to go beyond the screen boundaries
    if right_player.top <= 0:
        right_player.top = 0
    if right_player.bottom >= screen_height:
        right_player.bottom = screen_height
    # same as above
    if left_player.top <= 0:
        left_player.top = 0
    if left_player.bottom >= screen_height:
        left_player.bottom = screen_height


def animate_ball():
    # move around the ball
    ball.x += ball_speed_x
    #ball.y += ball_speed_y


hit_left = False
hit_right = False

# move left or right at start of game

# ********************************************************************** MAIN EVENT LOOP *****************************************************************************
while True:  # ( do forever)
    # get everything thats happening
    for event in pygame.event.get():
        # handle the closing of window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if first:
        randomize_ball_direction()
    animate_ball()
    handle_ball_bouncing()
    handle_player_boundaries()
    handle_player_points()
    # black background
    screen.fill("black")

    draw_players()
    display_score()
    draw_ball()
    handle_keys()
    pygame.display.update()

    # cap fps at 60
    clock.tick(60)
