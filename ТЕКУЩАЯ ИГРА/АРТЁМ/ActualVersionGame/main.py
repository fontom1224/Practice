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

# Шрифты для меню
font_title = pygame.font.Font(None, 72)
font_button = pygame.font.Font(None, 48)

# Загрузка звуков
try:
    boom_sound = pygame.mixer.Sound('assets/Boom.mp3')
    dead_asteroid_sound = pygame.mixer.Sound('assets/DeadAsteroid.mp3')
    shoot_sound = pygame.mixer.Sound('assets/OneShoot.mp3')
    powerup_sound = pygame.mixer.Sound('assets/PowerUp.mp3')
    heal_sound = pygame.mixer.Sound('assets/Heal.mp3')
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
    heal_sound = None


def show_story():
    """Показывает слайд-шоу из 4 изображений"""
    story_images = []
    for i in range(1, 5):
        try:
            img = pygame.image.load(f'assets/frame{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            story_images.append(img)
        except FileNotFoundError:
            print(f"Не найден файл frame{i}.png, пропускаем")
    if not story_images:
        return

    pygame.mixer.music.pause()

    idx = 0
    while idx < len(story_images):
        screen.blit(story_images[idx], (0, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        idx = len(story_images)
                    else:
                        waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        idx += 1

    pygame.mixer.music.unpause()


def show_menu():
    """Показывает меню и возвращает True если играть, False если выход"""
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    story_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

    while True:
        screen.blit(bg_image, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("ASTEROID SHOOTER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Кнопка ИГРАТЬ
        play_color = (50, 50, 200) if play_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, play_color, play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 2)
        play_text = font_button.render("ИГРАТЬ", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_rect)

        # Кнопка СЮЖЕТ
        story_color = (50, 200, 50) if story_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, story_color, story_button)
        pygame.draw.rect(screen, (255, 255, 255), story_button, 2)
        story_text = font_button.render("СЮЖЕТ", True, (255, 255, 255))
        story_rect = story_text.get_rect(center=story_button.center)
        screen.blit(story_text, story_rect)

        # Кнопка ВЫХОД
        quit_color = (200, 50, 50) if quit_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, quit_color, quit_button)
        pygame.draw.rect(screen, (255, 255, 255), quit_button, 2)
        quit_text = font_button.render("ВЫХОД", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                if story_button.collidepoint(event.pos):
                    show_story()
                if quit_button.collidepoint(event.pos):
                    return False


def reset_game():
    """Сброс игры"""
    global all_sprites, bullets, asteroids, heart_sprites, bosses, boss_bullets
    global powerups, medkits, enemy_planes, laser_bullets, net_bullets
    global diag_bullets, homing_bullets, ship, lives, score, medkits_collected
    global boss1_spawned, boss2_spawned, planes_spawned, asteroid_spawn_enabled
    global powerup_active, powerup_end_time, current_shot_delay, last_shot_time, next_asteroid_spawn

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    heart_sprites = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    medkits = pygame.sprite.Group()
    enemy_planes = pygame.sprite.Group()
    laser_bullets = pygame.sprite.Group()
    net_bullets = pygame.sprite.Group()
    diag_bullets = pygame.sprite.Group()
    homing_bullets = pygame.sprite.Group()

    ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
    all_sprites.add(ship)

    lives = 5
    score = 0
    medkits_collected = 0
    boss1_spawned = False
    boss2_spawned = False
    planes_spawned = False
    asteroid_spawn_enabled = True
    powerup_active = False
    powerup_end_time = 0
    current_shot_delay = 500
    last_shot_time = 0            # сброс времени последнего выстрела
    next_asteroid_spawn = pygame.time.get_ticks() + 500   # спавн через 0.5 сек

    update_hearts()


def update_hearts():
    """Обновляет отображение сердец"""
    for heart in heart_sprites:
        heart.kill()
    heart_sprites.empty()

    for i in range(lives):
        heart = Hp(10 + i * 40, 10)
        heart_sprites.add(heart)
        all_sprites.add(heart)


# Показываем меню перед игрой
if not show_menu():
    pygame.quit()
    exit()

# Инициализация игры
reset_game()

# Константы
BASE_SHOT_DELAY = 500
POWERUP_DURATION = 8000
SHOT_DELAY_BOOST = 250

running = True
space_pressed = False
font = pygame.font.Font(None, 36)

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

            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    space_pressed = False
                else:
                    running = False
                pygame.mixer.music.unpause()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    current_time = pygame.time.get_ticks()
    if powerup_active and current_time >= powerup_end_time:
        powerup_active = False
        current_shot_delay = BASE_SHOT_DELAY

    if space_pressed:
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
    medkits.update()
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

    # Спавн астероидов (таймер на основе реального времени)
    if asteroid_spawn_enabled and current_time >= next_asteroid_spawn:
        asteroid_type = random.choices([1, 2], weights=[70, 30])[0]
        asteroid = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        next_asteroid_spawn = current_time + random.randint(400, 700)  # 0.4-0.7 сек

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

                if random.random() < 0.01:
                    medkit = Medkit(asteroid.rect.centerx, asteroid.rect.centery)
                    all_sprites.add(medkit)
                    medkits.add(medkit)

                if asteroid.asteroid_type == 2:
                    pos1_x = max(0, min(asteroid.rect.centerx - 20, WIDTH - 40))
                    pos2_x = max(0, min(asteroid.rect.centerx + 20, WIDTH - 40))
                    small_asteroid1 = Asteroid(pos1_x, 1, vx=-2)
                    small_asteroid2 = Asteroid(pos2_x, 1, vx=2)
                    small_asteroid1.rect.y = asteroid.rect.centery
                    small_asteroid2.rect.y = asteroid.rect.centery
                    all_sprites.add(small_asteroid1, small_asteroid2)
                    asteroids.add(small_asteroid1, small_asteroid2)
                asteroid.kill()
            # break удалён – пуля может поразить несколько астероидов

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
                    # правильное удаление пуль босса
                    for b in list(boss_bullets):
                        b.kill()
                    boss_bullets.empty()
                    medkit = Medkit(boss.rect.centerx, boss.rect.centery)
                    all_sprites.add(medkit)
                    medkits.add(medkit)
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

                if isinstance(boss, GodBoss) and not planes_spawned:
                    planes_spawned = True
                    blue = BluePlane(0, 0)
                    green = GreenPlane(0, 0)
                    red = RedPlane(0, 0)
                    yellow = YellowPlane(0, 0)

                    for plane in [blue, green, red, yellow]:
                        plane.player = ship

                    center_x = boss.rect.centerx
                    center_y = boss.rect.centery
                    blue.start_launch(center_x, center_y, -3, -2, 40)
                    green.start_launch(center_x, center_y, 3, -2, 40)
                    red.start_launch(center_x, center_y, -2, 2, 40)
                    yellow.start_launch(center_x, center_y, 2, 2, 40)

                    all_sprites.add(blue, green, red, yellow)
                    enemy_planes.add(blue, green, red, yellow)
            break   # одна пуля – один босс, break оставляем

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

    # Сбор бонусов
    collected = pygame.sprite.spritecollide(ship, powerups, True)
    for powerup in collected:
        if powerup_sound:
            powerup_sound.play()
        powerup_active = True
        powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
        current_shot_delay = SHOT_DELAY_BOOST

    # Сбор аптечек (добавляем одно сердце, не более 5)
    collected_medkits = pygame.sprite.spritecollide(ship, medkits, True)
    for medkit in collected_medkits:
        if heal_sound:
            heal_sound.play()
        if lives < 5:
            lives = min(lives + 1, 5)
            update_hearts()
            medkits_collected += 1

    # Столкновение корабля с астероидами
    if pygame.sprite.spritecollide(ship, asteroids, True):
        if not ship.invincible:
            lives -= 1
            ship.set_invincible(2000)
            if lives <= 0:
                if boom_sound:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    space_pressed = False
                else:
                    running = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

    # Столкновение с пулями боссов
    if pygame.sprite.spritecollide(ship, boss_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Столкновение с лазерными пулями
    if pygame.sprite.spritecollide(ship, laser_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
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
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Столкновение с самонаводящимися пулями
    if pygame.sprite.spritecollide(ship, homing_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
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
        asteroid_spawn_enabled = False

    # Если самолёты были созданы и все уничтожены – возобновляем спавн астероидов
    if planes_spawned and len(enemy_planes) == 0 and not asteroid_spawn_enabled:
        asteroid_spawn_enabled = True

    all_sprites.draw(screen)

    # Полоски здоровья боссов
    for boss in bosses:
        max_health = 20 if isinstance(boss, GodBoss) else 10
        health_percent = boss.health / max_health
        bar_width = 200
        bar_height = 15
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 35
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
        boss_text = font.render("БОСС", True, (255, 100, 100))
        screen.blit(boss_text, (WIDTH // 2 - 30, 15))

    # Полоски здоровья самолётов
    for plane in enemy_planes:
        health_percent = plane.health / 3
        bar_width = 40
        bar_height = 6
        bar_x = plane.rect.centerx - bar_width // 2
        bar_y = plane.rect.top - 10
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))

    # Отображение счёта
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    medkit_text = font.render(f"Аптечки: {medkits_collected}", True, (255, 255, 255))
    screen.blit(medkit_text, (10, 90))

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
