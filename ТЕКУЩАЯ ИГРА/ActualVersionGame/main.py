import pygame
import random
from sprites import *

pygame.init()
pygame.mixer.init()

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
bosses = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()  # группа для пуль босса

ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
all_sprites.add(ship)

lives = 3
score = 0
font = pygame.font.Font(None, 36)

# Флаг, появился ли уже босс (чтобы не спавнить несколько)
boss1_spawned = False


def update_hearts():
    heart_sprites.empty()
    for i in range(lives):
        heart = Hp(10 + i * 40, 10)
        heart_sprites.add(heart)
        all_sprites.add(heart)


update_hearts()

spawn_timer = 0

# Стрельба с задержкой
space_pressed = False
last_shot_time = 0
SHOT_DELAY = 500

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

    # Автострельба
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

    # Обновление боссов и их стрельба
    for boss in bosses:
        if boss.update():  # если пора стрелять
            boss_bullet = BossBullet(boss.rect.centerx, boss.rect.bottom)
            all_sprites.add(boss_bullet)
            boss_bullets.add(boss_bullet)
    boss_bullets.update()

    # Спавн астероидов
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        asteroid_type = random.choices([1, 2], weights=[70, 30])[0]
        asteroid = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # --- Столкновения пуль игрока с астероидами ---
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, asteroids, False)
        for asteroid in collided:
            bullet.kill()
            if asteroid.take_damage():
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
                score += asteroid.points

                # Если это большой метеорит, создаём два маленьких
                if asteroid.asteroid_type == 2:
                    # Создаём два маленьких метеорита на месте большого
                    small_asteroid1 = Asteroid(asteroid.rect.centerx - 20, 1)
                    small_asteroid2 = Asteroid(asteroid.rect.centerx + 20, 1)
                    small_asteroid1.rect.y = asteroid.rect.centery
                    small_asteroid2.rect.y = asteroid.rect.centery
                    all_sprites.add(small_asteroid1, small_asteroid2)
                    asteroids.add(small_asteroid1, small_asteroid2)
                asteroid.kill()
            break

    # --- Столкновения пуль игрока с боссом ---
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, bosses, False)
        for boss in collided:
            bullet.kill()
            if boss.take_damage():
                score += boss.points  # босс уничтожен, можно спавнить нового
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
            break

    # --- Столкновение корабля с астероидами ---
    if pygame.sprite.spritecollide(ship, asteroids, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            running = False
        else:
            for heart in heart_sprites:
                heart.kill()
            heart_sprites.empty()
            update_hearts()

    # --- Столкновение корабля с пулями босса ---
    if pygame.sprite.spritecollide(ship, boss_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            running = False
        else:
            for heart in heart_sprites:
                heart.kill()
            heart_sprites.empty()
            update_hearts()

    # --- Спавн босса при достижении 250 очков (один раз) ---
    if score >= 250 and not boss1_spawned and len(bosses) == 0:
        boss = Boss(random.randint(100, WIDTH - 100), 50)
        all_sprites.add(boss)
        bosses.add(boss)
        boss1_spawned = True

    # Отрисовка
    all_sprites.draw(screen)

    # Отображение счёта
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
