import pygame
import random
from sprites import Ship, Bullet, Asteroid, Hp

pygame.init()
pygame.mixer.init()  # Инициализация звука

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()
bg_original = pygame.image.load('assets/fon.png')
bg_image = pygame.transform.scale(bg_original, (800, 600))

# Загрузка звуков
try:
    boom_sound = pygame.mixer.Sound('assets/Boom.mp3')
    dead_asteroid_sound = pygame.mixer.Sound('assets/DeadAsteroid.mp3')
    shoot_sound = pygame.mixer.Sound('assets/OneShoot.mp3')
    pygame.mixer.music.load('assets/Music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    print("Звуки загружены успешно")
except FileNotFoundError as e:
    print(f"Ошибка: не найден звуковой файл - {e}")
    boom_sound = None
    dead_asteroid_sound = None
    shoot_sound = None


# Группы спрайтов
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
heart_sprites = pygame.sprite.Group()

ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
all_sprites.add(ship)

lives = 3


def update_hearts():
    heart_sprites.empty()
    for i in range(lives):
        heart = Hp(10 + i * 40, 10)
        heart_sprites.add(heart)
        all_sprites.add(heart)


update_hearts()

score = 0
font = pygame.font.Font(None, 36)

spawn_timer = 0

# Переменные для стрельбы с задержкой
space_pressed = False
last_shot_time = 0
SHOT_DELAY = 500  # 500 миллисекунд = 0.5 секунды


running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    screen.blit(bg_image, (0, 0))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
                # Мгновенный выстрел при первом нажатии
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= SHOT_DELAY:
                    bullet = Bullet(ship.rect.centerx, ship.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    if shoot_sound:
                        shoot_sound.play()
                    last_shot_time = current_time
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    # Автоматическая стрельба при зажатой кнопке
    if space_pressed:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time >= SHOT_DELAY:
            bullet = Bullet(ship.rect.centerx, ship.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if shoot_sound:
                shoot_sound.play()
            last_shot_time = current_time

    # Обновление спрайтов
    keys = pygame.key.get_pressed()
    ship.update(keys)
    bullets.update()
    asteroids.update()

    # Спавн астероидов
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        asteroid_type = random.choices([1, 2], weights=[70, 30])[0]
        asteroid = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # Столкновения пуль с астероидами
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, asteroids, False)
        for asteroid in collided:
            bullet.kill()
            if asteroid.take_damage():
                # звук уничтожения астероида
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
                score += asteroid.points
            break  # одна пуля – один астероид

    # Столкновение корабля с астероидами
    dtp = pygame.sprite.spritecollide(ship, asteroids, True)
    if dtp:
        lives -= 1
        if lives <= 0:
            # звук взрыва корабля 
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)  # Небольшая задержка перед закрытием
            running = False
        else:
            # Очищаем старые сердечки и обновляем
            for heart in heart_sprites:
                heart.kill()
            heart_sprites.empty()
            update_hearts()

            # Отрисовка
    all_sprites.draw(screen)

    # Отображение счёта
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    pygame.display.flip()

# Останавливаем музыку при выходе
pygame.mixer.music.stop()
pygame.quit()