import pygame
import os

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")

# play the music
pygame.mixer.init()

SONG = pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'song.wav'))
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 40)

PONG_WIDTH, PONG_HEIGHT = 10, 50
BALL_WIDTH, BALL_HEIGHT = 10, 10

VEL = 5
BALL_VEL = 3.0

ORANGE_PONG_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Sprites', 'orange.png'))
PINK_PONG_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Sprites', 'pink.png'))
BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'Sprites', 'ball.png'))

ORANGE_PONG = pygame.transform.rotate(pygame.transform.scale(
    ORANGE_PONG_IMAGE, (PONG_WIDTH, PONG_HEIGHT)), 0)
PINK_PONG = pygame.transform.rotate(pygame.transform.scale(
    PINK_PONG_IMAGE, (PONG_WIDTH, PONG_HEIGHT)), 0)
BALL = pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

PING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', "ping.wav"))
PONG_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', "pong.wav"))
EXPLODE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Sounds', "explode.wav"))

FPS = 60


def draw(orange, pink, ball, orange_score, pink_score):
    WIN.fill((0, 0, 0))
    WIN.blit(ORANGE_PONG, (orange.x, orange.y))
    WIN.blit(PINK_PONG, (pink.x, pink.y))
    WIN.blit(BALL, (ball.x, ball.y))

    orange_score_text = FONT.render(
        str(orange_score), 1, (255, 255, 255))
    pink_score_text = FONT.render(
        str(pink_score), 0.3, (255, 255, 255))
    credits_text = FONT.render("(c) Gargant 2022", 1, (255, 255, 255))
    credits_text = pygame.transform.scale(credits_text, (int(
        credits_text.get_width() * 0.3), int(credits_text.get_height() * 0.3)))

    WIN.blit(orange_score_text, (WIDTH/2 - 50, 10))
    WIN.blit(pink_score_text, (WIDTH/2 + 50, 10))
    WIN.blit(credits_text, (WIDTH - credits_text.get_width() -
             10, HEIGHT - credits_text.get_height() - 10))

    pygame.display.update()


def play_ping():
    pygame.mixer.Sound.play(PING_SOUND)


def play_pong():
    pygame.mixer.Sound.play(PONG_SOUND)


def play_explode():
    pygame.mixer.Sound.play(EXPLODE_SOUND)


def check_movement(orange, pink, keys_pressed):
    if keys_pressed[pygame.K_w]:
        orange.y -= 5
        if (orange.y < 0):
            orange.y = 0
    if keys_pressed[pygame.K_s]:
        orange.y += 5
        if (orange.y > HEIGHT - PONG_HEIGHT):
            orange.y = HEIGHT - PONG_HEIGHT
    if keys_pressed[pygame.K_UP]:
        pink.y -= 5
        if (pink.y < 0):
            pink.y = 0
    if keys_pressed[pygame.K_DOWN]:
        pink.y += 5
        if (pink.y > HEIGHT - PONG_HEIGHT):
            pink.y = HEIGHT - PONG_HEIGHT


def handle_ball_movement(ball, orange, pink, ball_x_direction, ball_y_direction, orange_score, pink_score):
    middle_ball_y = ball.y + BALL_HEIGHT/2
    middle_orange_y = orange.y + PONG_HEIGHT/2
    middle_pink_y = pink.y + PONG_HEIGHT/2

    # out of bor
    if ball.x < 0:
        ball.x = WIDTH/2
        ball.y = HEIGHT/2
        ball_x_direction *= -1
        ball_y_direction = 0
        pink_score += 1
        play_explode()
    elif ball.x > WIDTH:
        ball.x = WIDTH/2
        ball.y = HEIGHT/2
        ball_x_direction *= - 1
        ball_y_direction = 0
        orange_score += 1
        play_explode()
    if ball.y < 0 or ball.y > HEIGHT:
        ball_y_direction *= -1
        play_pong()

    # ball collision with orange
    if ball.colliderect(orange):
        ball_y_direction = (middle_ball_y - middle_orange_y) / 15
        ball_x_direction = 1
        play_ping()

    # ball collision with pink
    if ball.colliderect(pink):
        ball_y_direction = (middle_ball_y - middle_pink_y) / 15
        ball_x_direction = -1
        play_ping()

    ball.x += ball_x_direction * BALL_VEL
    ball.y += ball_y_direction * BALL_VEL
    return (ball_x_direction, ball_y_direction, orange_score, pink_score)


def main():
    run = True
    clock = pygame.time.Clock()

    orange_score = 0
    pink_score = 0

    orange = pygame.Rect(WIDTH/20, HEIGHT/2 -
                         PONG_HEIGHT / 2, PONG_WIDTH, PONG_HEIGHT)
    pink = pygame.Rect(WIDTH - WIDTH/20, HEIGHT/2 -
                       PONG_HEIGHT / 2, PONG_WIDTH, PONG_HEIGHT)
    ball = pygame.Rect(WIDTH/2, HEIGHT/2, BALL_WIDTH, BALL_HEIGHT)

    ball_x_direction = 1
    ball_y_direction = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        keys_pressed = pygame.key.get_pressed()
        draw(orange, pink, ball, orange_score, pink_score)
        check_movement(orange, pink, keys_pressed)
        ball_x_direction, ball_y_direction, orange_score, pink_score = handle_ball_movement(
            ball, orange, pink, ball_x_direction, ball_y_direction, orange_score, pink_score)


if __name__ == "__main__":
    main()
