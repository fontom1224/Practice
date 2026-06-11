import pygame
import random
import math
from sprites import *

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()
bg_original = pygame.image.load('assets/fon.png')
bg_image = pygame.transform.scale(bg_original, (800, 600))

try:
    boom_sound = pygame.mixer.Sound('assets/Boom.mp3')
    dead_asteroid_sound = pygame.mixer.Sound('assets/DeadAsteroid.mp3')
    shoot_sound = pygame.mixer.Sound('assets/OneShoot.mp3')
    powerup_sound = pygame.mixer.Sound('assets/PowerUp.mp3')
    pygame.mixer.music.load('assets/Music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    print("Звуки загружены успешно")
except FileNotFoundError as e:
    print(f"Ошибка: не найден звуковой файл - {e}")
    boom_sound = None
    dead_asteroid_sound = None
    shoot_sound = None
    powerup_sound = None

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
heart_sprites = pygame.sprite.Group()
bosses = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

enemy_planes = pygame.sprite.Group()
laser_bullets = pygame.sprite.Group()
net_bullets = pygame.sprite.Group()
diag_bullets = pygame.sprite.Group()
homing_bullets = pygame.sprite.Group()

ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
all_sprites.add(ship)

lives = 5
score = 0
font = pygame.font.Font(None, 36)

boss1_spawned = False
boss2_spawned = False
planes_spawned = False

# Флаг управления спавном астероидов
asteroid_spawn_enabled = True

space_pressed = False
last_shot_time = 0
BASE_SHOT_DELAY = 500
current_shot_delay = BASE_SHOT_DELAY

powerup_active = False
powerup_end_time = 0
POWERUP_DURATION = 8000
SHOT_DELAY_BOOST = 250

def update_hearts():
    heart_sprites.empty()
    for i in range(lives):
        heart = Hp(10 + i * 40, 10)
        heart_sprites.add(heart)
        all_sprites.add(heart)

update_hearts()
spawn_timer = 0
running = True

while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= current_shot_delay:
                    bullet = Bullet(ship.rect.centerx, ship.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    if shoot_sound:
                        shoot_sound.play()
                    last_shot_time = current_time
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    current_time = pygame.time.get_ticks()
    if powerup_active and current_time >= powerup_end_time:
        powerup_active = False
        current_shot_delay = BASE_SHOT_DELAY

    if space_pressed:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time >= current_shot_delay:
            bullet = Bullet(ship.rect.centerx, ship.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if shoot_sound:
                shoot_sound.play()
            last_shot_time = current_time

    keys = pygame.key.get_pressed()
    ship.update(keys)
    bullets.update()
    asteroids.update()
    powerups.update()
    enemy_planes.update()
    laser_bullets.update()
    net_bullets.update()
    diag_bullets.update()
    homing_bullets.update()
    boss_bullets.update()

    # Стрельба боссов
    for boss in bosses:
        if boss.update():
            if isinstance(boss, GodBoss):
                pattern = boss.attack_pattern
                if pattern == 0:
                    bullet = LaserBullet(boss.rect.centerx, boss.rect.bottom)
                    all_sprites.add(bullet)
                    laser_bullets.add(bullet)
                elif pattern == 1:
                    net = NetBullet(boss.rect.centerx, boss.rect.bottom)
                    all_sprites.add(net)
                    net_bullets.add(net)
                elif pattern == 2:
                    diag1 = DiagBullet(boss.rect.centerx, boss.rect.bottom, math.pi/4)
                    diag2 = DiagBullet(boss.rect.centerx, boss.rect.bottom, -math.pi/4)
                    all_sprites.add(diag1, diag2)
                    diag_bullets.add(diag1, diag2)
                elif pattern == 3:
                    homing = HomingBullet(boss.rect.centerx, boss.rect.bottom, ship)
                    all_sprites.add(homing)
                    homing_bullets.add(homing)
            else:
                boss_bullet = BossBullet(boss.rect.centerx, boss.rect.bottom)
                all_sprites.add(boss_bullet)
                boss_bullets.add(boss_bullet)

    # Стрельба самолётов
    for plane in enemy_planes:
        if plane.update():
            if isinstance(plane, BluePlane):
                bullet = LaserBullet(plane.rect.centerx, plane.rect.bottom)
                all_sprites.add(bullet)
                laser_bullets.add(bullet)
            elif isinstance(plane, GreenPlane):
                net = NetBullet(plane.rect.centerx, plane.rect.bottom)
                all_sprites.add(net)
                net_bullets.add(net)
            elif isinstance(plane, RedPlane):
                diag1 = DiagBullet(plane.rect.centerx, plane.rect.bottom, math.pi/4)
                diag2 = DiagBullet(plane.rect.centerx, plane.rect.bottom, -math.pi/4)
                all_sprites.add(diag1, diag2)
                diag_bullets.add(diag1, diag2)
            elif isinstance(plane, YellowPlane):
                homing = HomingBullet(plane.rect.centerx, plane.rect.bottom, ship)
                all_sprites.add(homing)
                homing_bullets.add(homing)

    # Спавн астероидов (только если разрешено)
    if asteroid_spawn_enabled:
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
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
                score += asteroid.points
                drop_chance = 0.3 if asteroid.asteroid_type == 2 else 0.15
                if random.random() < drop_chance:
                    powerup = PowerUp(asteroid.rect.centerx, asteroid.rect.centery)
                    all_sprites.add(powerup)
                    powerups.add(powerup)
                if asteroid.asteroid_type == 2:
                    pos1_x = max(0, min(asteroid.rect.centerx - 20, WIDTH - 40))
                    pos2_x = max(0, min(asteroid.rect.centerx + 20, WIDTH - 40))
                    small_asteroid1 = Asteroid(pos1_x, 1)
                    small_asteroid2 = Asteroid(pos2_x, 1)
                    small_asteroid1.rect.y = asteroid.rect.centery
                    small_asteroid2.rect.y = asteroid.rect.centery
                    all_sprites.add(small_asteroid1, small_asteroid2)
                    asteroids.add(small_asteroid1, small_asteroid2)
                asteroid.kill()
            break

    # Столкновения пуль с боссами
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, bosses, False)
        for boss in collided:
            bullet.kill()
            if boss.take_damage():
                score += boss.points
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()

                if isinstance(boss, Boss):
                    for b in list(boss_bullets):
                        b.kill()
                    boss_bullets.empty()
                elif isinstance(boss, GodBoss):
                    for b in list(laser_bullets):
                        b.kill()
                    for b in list(net_bullets):
                        b.kill()
                    for b in list(diag_bullets):
                        b.kill()
                    for b in list(homing_bullets):
                        b.kill()
                    laser_bullets.empty()
                    net_bullets.empty()
                    diag_bullets.empty()
                    homing_bullets.empty()

                # Спавн четырёх самолётов после смерти GodBoss
                if isinstance(boss, GodBoss) and not planes_spawned:
                    planes_spawned = True
                    blue = BluePlane(150, 100)
                    green = GreenPlane(300, 100)
                    red = RedPlane(450, 100)
                    yellow = YellowPlane(600, 100)
                    for plane in [blue, green, red, yellow]:
                        plane.player = ship
                    all_sprites.add(blue, green, red, yellow)
                    enemy_planes.add(blue, green, red, yellow)
            break

    # Столкновения пуль с самолётами
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, enemy_planes, False)
        for plane in collided:
            bullet.kill()
            if plane.take_damage():
                score += plane.points
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
            break

    # Столкновения пуль с жёлтыми самонаводящимися пулями
    for bullet in bullets:
        collided = pygame.sprite.spritecollide(bullet, homing_bullets, True)
        for homing in collided:
            bullet.kill()
            break

    # Столкновение корабля с бонусами
    collected = pygame.sprite.spritecollide(ship, powerups, True)
    for powerup in collected:
        if powerup_sound:
            powerup_sound.play()
        powerup_active = True
        powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
        current_shot_delay = SHOT_DELAY_BOOST

    # Столкновение корабля с астероидами
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

    # Столкновение с пулями боссов
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

    # Столкновение с лазерными пулями
    if pygame.sprite.spritecollide(ship, laser_bullets, True):
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

    # Столкновение с сетью
    net_hits = pygame.sprite.spritecollide(ship, net_bullets, True)
    for net in net_hits:
        ship.slow_timer = 180

    # Столкновение с диагональными пулями
    if pygame.sprite.spritecollide(ship, diag_bullets, True):
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

    # Столкновение с самонаводящимися пулями
    if pygame.sprite.spritecollide(ship, homing_bullets, True):
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

    # Спавн первого босса
    if score >= 250 and not boss1_spawned and len(bosses) == 0 and not boss2_spawned:
        boss = Boss(random.randint(100, WIDTH - 100), 50)
        all_sprites.add(boss)
        bosses.add(boss)
        boss1_spawned = True

    # Спавн второго босса – отключаем спавн астероидов
    if score >= 750 and not boss2_spawned and len(bosses) == 0 and not planes_spawned:
        god = GodBoss(random.randint(100, WIDTH - 100), 50)
        all_sprites.add(god)
        bosses.add(god)
        boss2_spawned = True
        asteroid_spawn_enabled = False   # астероиды больше не спавнятся
        print("Второй босс появился! Спавн астероидов остановлен.")

    # Если самолёты были созданы и все уничтожены – возобновляем спавн астероидов
    if planes_spawned and len(enemy_planes) == 0 and not asteroid_spawn_enabled:
        asteroid_spawn_enabled = True
        print("Все самолёты уничтожены! Спавн астероидов возобновлён.")

    all_sprites.draw(screen)

    # Полоски здоровья боссов
    for boss in bosses:
        max_health = 20 if isinstance(boss, GodBoss) else 10
        health_percent = boss.health / max_health
        bar_width = 200
        bar_height = 15
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 20
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
        boss_text = font.render("БОСС", True, (255, 100, 100))
        screen.blit(boss_text, (WIDTH // 2 - 30, 5))

    # Полоски здоровья самолётов
    for plane in enemy_planes:
        health_percent = plane.health / 3
        bar_width = 40
        bar_height = 6
        bar_x = plane.rect.centerx - bar_width // 2
        bar_y = plane.rect.top - 10
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))

    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    if powerup_active:
        time_left = max(0, (powerup_end_time - pygame.time.get_ticks()) // 1000)
        boost_text = font.render(f"УСКОРЕНИЕ: {time_left}с", True, (0, 255, 0))
        screen.blit(boost_text, (WIDTH - 180, 10))
        powerup_percent = (powerup_end_time - pygame.time.get_ticks()) / POWERUP_DURATION
        bar_width = 150
        bar_height = 8
        bar_x = WIDTH - 170
        bar_y = 40
        pygame.draw.rect(screen, (0, 100, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * powerup_percent, bar_height))

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
