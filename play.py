import pygame

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PONG_WIDTH, PONG_HEIGHT = 10, 50
BALL_WIDTH, BALL_HEIGHT = 10, 10

VEL = 5
BALL_VEL = 3.0

ORANGE_PONG_IMAGE = pygame.image.load('orange.png')
PINK_PONG_IMAGE = pygame.image.load('pink.png')
BALL_IMAGE = pygame.image.load('ball.png')

ORANGE_PONG = pygame.transform.rotate(pygame.transform.scale(
    ORANGE_PONG_IMAGE, (PONG_WIDTH, PONG_HEIGHT)), 0)
PINK_PONG = pygame.transform.rotate(pygame.transform.scale(
    PINK_PONG_IMAGE, (PONG_WIDTH, PONG_HEIGHT)), 0)
BALL = pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

FPS = 60

def draw(orange, pink, ball):
    WIN.fill((0, 0, 0))
    WIN.blit(ORANGE_PONG, (orange.x, orange.y))
    WIN.blit(PINK_PONG, (pink.x, pink.y))
    WIN.blit(BALL, (ball.x, ball.y))
    pygame.display.update()


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


def handle_ball_movement(ball, orange, pink, ball_x_direction, ball_y_direction):
    middle_ball_y = ball.y + BALL_HEIGHT/2
    middle_orange_y = orange.y + PONG_HEIGHT/2
    middle_pink_y = pink.y + PONG_HEIGHT/2
    
    # out of bor
    if ball.x < 0:
        ball.x = WIDTH/2
        ball.y = HEIGHT/2
        ball_x_direction *= -1
        ball_y_direction = 0
    elif ball.x > WIDTH:
        ball.x = WIDTH/2
        ball.y = HEIGHT/2
        ball_x_direction *= - 1
        ball_y_direction = 0
    if ball.y < 0 or ball.y > HEIGHT:
        ball_y_direction *= -1
    
    # ball collision with orange
    if ball.colliderect(orange):
        if abs(middle_ball_y - middle_pink_y) > 15:
            if middle_ball_y > middle_orange_y:
                ball_y_direction = 1
            else:
                ball_y_direction = -1
        else:
            ball_y_direction = 0
        ball_x_direction = 1
    
    # ball collision with pink
    if ball.colliderect(pink):
        if abs(middle_ball_y - middle_pink_y) > 15:
            if middle_ball_y > middle_pink_y:
                ball_y_direction = 1
            else:
                ball_y_direction = -1
        else:
            ball_y_direction = 0
        ball_x_direction = -1

    ball.x += ball_x_direction * BALL_VEL
    ball.y += ball_y_direction * BALL_VEL
    return (ball_x_direction, ball_y_direction)


def main():
    run = True
    clock = pygame.time.Clock()

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
        draw(orange, pink, ball)
        check_movement(orange, pink, keys_pressed)
        ball_x_direction, ball_y_direction = handle_ball_movement(ball, orange, pink, ball_x_direction, ball_y_direction)


if __name__ == "__main__":
    main()
