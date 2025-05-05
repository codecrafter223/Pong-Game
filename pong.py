import pygame

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1500, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
CLOCK = pygame.time.Clock()
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de paletas
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 150
PADDLE_SPEED = 10
PADDLE1 = pygame.Rect(25, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
PADDLE2 = pygame.Rect(WIDTH - 45, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Configuración de la pelota
BALL_RADIUS = 17
BALL_X, BALL_Y = WIDTH // 2, HEIGHT // 2
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Puntajes
score1, score2 = 0, 0
FONT = pygame.font.SysFont("Arial", 40)

def draw_objects():
    """Dibuja los objetos en la pantalla."""
    SCREEN.fill(BLACK)
    score_text_1 = FONT.render(f"{score1}", True, WHITE)
    score_text_2 = FONT.render(f"{score2}", True, WHITE)
    SCREEN.blit(score_text_1, (WIDTH // 4, 40))
    SCREEN.blit(score_text_2, (WIDTH * 3 // 4, 40))
    pygame.draw.rect(SCREEN, WHITE, PADDLE1)
    pygame.draw.rect(SCREEN, WHITE, PADDLE2)
    pygame.draw.line(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    return pygame.draw.circle(SCREEN, WHITE, (BALL_X, BALL_Y), BALL_RADIUS, 0)

def move_paddles():
    """Mueve las paletas según la entrada del usuario."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and PADDLE1.top > 0:
        PADDLE1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and PADDLE1.bottom < HEIGHT:
        PADDLE1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and PADDLE2.top > 0:
        PADDLE2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and PADDLE2.bottom < HEIGHT:
        PADDLE2.y += PADDLE_SPEED

def move_ball():
    """Mueve la pelota y detecta colisiones."""
    global BALL_X, BALL_Y, BALL_SPEED_X, BALL_SPEED_Y, score1, score2
    BALL_X += BALL_SPEED_X
    BALL_Y += BALL_SPEED_Y
    
    if BALL_Y - BALL_RADIUS <= 0 or BALL_Y + BALL_RADIUS >= HEIGHT:
        BALL_SPEED_Y *= -1
    if BALL_X - BALL_RADIUS <= 0:
        score2 += 1
        reset_ball()
    elif BALL_X + BALL_RADIUS >= WIDTH:
        score1 += 1
        reset_ball()

def reset_ball():
    """Reinicia la posición de la pelota."""
    global BALL_X, BALL_Y, BALL_SPEED_X, BALL_SPEED_Y
    BALL_X, BALL_Y = WIDTH // 2, HEIGHT // 2
    BALL_SPEED_X = 5 if BALL_SPEED_X > 0 else -5
    BALL_SPEED_Y = 5 if BALL_SPEED_Y > 0 else -5

def main():
    """Bucle principal del juego."""
    global BALL_SPEED_X, BALL_SPEED_Y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        move_paddles()
        move_ball()
        ball = draw_objects()
        
        if ball.colliderect(PADDLE1) or ball.colliderect(PADDLE2):
            BALL_SPEED_X *= -1.1  # Aumenta la velocidad tras cada rebote
            offset = (BALL_Y - (PADDLE1.y if ball.colliderect(PADDLE1) else PADDLE2.y)) / PADDLE_HEIGHT
            BALL_SPEED_Y += offset * 2  # Modifica la trayectoria de rebote
        
        pygame.display.flip()
        CLOCK.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
