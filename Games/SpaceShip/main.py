import pygame
import random
from sprites import Ship, Bullet, Asteroid, Asteroidbr

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Создание корабля
ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
all_sprites.add(ship)

# Счёт
score = 0
font = pygame.font.Font(None, 36)

# Таймер для спавна астероидов
spawn_timer = 0

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(ship.rect.centerx, ship.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Обновление
    keys = pygame.key.get_pressed()
    ship.update(keys)
    bullets.update()
    asteroids.update()

    # Спавн астероидов
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        # Вероятность: 70 % — маленькие, 30 % — большие
        asteroid_type = random.choices(
            [1, 2],
            weights=[70, 30]  # Веса определяют вероятность
        )[0]
        asteroid = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # Столкновения
    hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    for bullet in bullets:
        # Проверяем столкновения пули с каждым астероидом
        collided_asteroids = pygame.sprite.spritecollide(bullet, asteroids, False)
        for asteroid in collided_asteroids:
            # Пуля уничтожается при попадании
            bullet.kill()
            # Астероид получает урон
            asteroid.take_damage()
            # Начисляем очки в зависимости от типа
            if asteroid.asteroid_type == 1:
                score += 10
            else:
                score += 30
            break  # Выходим после первого столкновения

    if pygame.sprite.spritecollideany(ship, asteroids):
        running = False

    # Отрисовка
    all_sprites.draw(screen)

    # Отображение счёта
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
