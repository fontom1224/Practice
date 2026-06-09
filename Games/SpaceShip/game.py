import pygame
import random

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Корабль
ship_width, ship_height = 50, 50
ship_x = WIDTH // 2 - ship_width // 2
ship_y = HEIGHT - ship_height - 10
ship_speed = 5

# Пули
bullets = []
bullet_width, bullet_height = 5, 10
bullet_speed = -7

# Астероиды
asteroids = []
asteroid_width, asteroid_height = 40, 40
asteroid_speed = 3
spawn_timer = 0

# Счёт
score = 0
font = pygame.font.Font(None, 36)

# Загрузка спрайтов (пока сделаем цветными квадратами, потом замените на свои картинки)
# Вы потом замените эти квадраты на свои спрайты: ship_img, asteroid_img, bullet_img

running = True
while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(ship_x + ship_width//2 - bullet_width//2, ship_y, bullet_width, bullet_height))
    
    # Управление кораблём
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 0:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < WIDTH - ship_width:
        ship_x += ship_speed
    
    # Движение пуль
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y + bullet_height < 0:
            bullets.remove(bullet)
    
    # Спавн астероидов
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        asteroid_x = random.randint(0, WIDTH - asteroid_width)
        asteroids.append(pygame.Rect(asteroid_x, -asteroid_height, asteroid_width, asteroid_height))
    
    # Движение астероидов
    for asteroid in asteroids[:]:
        asteroid.y += asteroid_speed
        if asteroid.y > HEIGHT:
            asteroids.remove(asteroid)
    
    # Столкновения пуль с астероидами
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += 10
                break
    
    # Столкновение корабля с астероидом
    ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
    for asteroid in asteroids[:]:
        if ship_rect.colliderect(asteroid):
            running = False  # Игра заканчивается при столкновении
    
    # Отрисовка
    pygame.draw.rect(screen, (0, 255, 0), ship_rect)  # корабль (замените на спрайт)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)  # пули
    for asteroid in asteroids:
        pygame.draw.rect(screen, (150, 75, 0), asteroid)  # астероиды
    
    # Отображение счёта
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
