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
font_settings = pygame.font.Font(None, 36)

# Настройки звука
music_volume = 1.0
sfx_volume = 1.0

# Загрузка звуков
try:
    boom_sound = pygame.mixer.Sound('assets/Boom.mp3')
    dead_asteroid_sound = pygame.mixer.Sound('assets/DeadAsteroid.mp3')
    shoot_sound = pygame.mixer.Sound('assets/OneShoot.mp3')
    powerup_sound = pygame.mixer.Sound('assets/PowerUp.mp3')
    medkit_sound = pygame.mixer.Sound('assets/Medkit.mp3')
    dark_sound = pygame.mixer.Sound('assets/DarkSouls.mp3')
    spawn_sound = pygame.mixer.Sound('assets/terraria.mp3')
    transform_sound = pygame.mixer.Sound('assets/transform.mp3')

    shoot_sound.set_volume(0.3)
    medkit_sound.set_volume(1)
    spawn_sound.set_volume(1)
    dark_sound.set_volume(0.2)

    pygame.mixer.music.load('assets/Music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except FileNotFoundError as e:
    print(f"Ошибка: не найден звуковой файл - {e}")
    boom_sound = None
    dead_asteroid_sound = None
    shoot_sound = None
    powerup_sound = None
    medkit_sound = None


def set_volumes():
    pygame.mixer.music.set_volume(music_volume)
    if dark_sound:
        dark_sound.set_volume(music_volume)
    if boom_sound:
        boom_sound.set_volume(sfx_volume)
    if dead_asteroid_sound:
        dead_asteroid_sound.set_volume(sfx_volume)
    if shoot_sound:
        shoot_sound.set_volume(sfx_volume)
    if powerup_sound:
        powerup_sound.set_volume(sfx_volume)
    if medkit_sound:
        medkit_sound.set_volume(sfx_volume)
    if transform_sound:
        transform_sound.set_volume(sfx_volume)



def show_settings():
    global music_volume, sfx_volume

    music_minus = pygame.Rect(WIDTH // 2 - 185, HEIGHT // 2 - 60, 50, 50)
    music_plus = pygame.Rect(WIDTH // 2 + 140, HEIGHT // 2 - 60, 50, 50)
    sfx_minus = pygame.Rect(WIDTH // 2 - 185, HEIGHT // 2 + 20, 50, 50)
    sfx_plus = pygame.Rect(WIDTH // 2 + 140, HEIGHT // 2 + 20, 50, 50)
    back_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 130, 240, 60)

    dragging_music = False
    dragging_sfx = False

    while True:
        screen.blit(bg_image, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 150, 500, 350)
        pygame.draw.rect(screen, (50, 50, 50), panel)
        pygame.draw.rect(screen, (255, 255, 255), panel, 3)

        title = font_title.render("НАСТРОЙКИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        music_text = font_settings.render(f"МУЗЫКА: {int(music_volume * 100)}%", True, (255, 255, 255))
        music_rect = music_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(music_text, music_rect)

        music_minus_color = (150, 50, 50) if music_minus.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, music_minus_color, music_minus)
        pygame.draw.rect(screen, (255, 255, 255), music_minus, 2)
        minus_text = font_settings.render("-", True, (255, 255, 255))
        minus_rect = minus_text.get_rect(center=music_minus.center)
        screen.blit(minus_text, minus_rect)

        music_plus_color = (50, 150, 50) if music_plus.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, music_plus_color, music_plus)
        pygame.draw.rect(screen, (255, 255, 255), music_plus, 2)
        plus_text = font_settings.render("+", True, (255, 255, 255))
        plus_rect = plus_text.get_rect(center=music_plus.center)
        screen.blit(plus_text, plus_rect)

        bar_x = WIDTH // 2 - 120
        bar_y = HEIGHT // 2 - 50
        bar_width = 240
        bar_height = 10
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * music_volume, bar_height))

        circle_x = bar_x + bar_width * music_volume
        pygame.draw.circle(screen, (255, 255, 255), (int(circle_x), bar_y + bar_height // 2), 10)

        if dragging_music:
            music_volume = max(0, min(1, (mouse_pos[0] - bar_x) / bar_width))
            set_volumes()

        sfx_text = font_settings.render(f"ЗВУКИ: {int(sfx_volume * 100)}%", True, (255, 255, 255))
        sfx_rect = sfx_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(sfx_text, sfx_rect)

        sfx_minus_color = (150, 50, 50) if sfx_minus.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, sfx_minus_color, sfx_minus)
        pygame.draw.rect(screen, (255, 255, 255), sfx_minus, 2)
        minus_text2 = font_settings.render("-", True, (255, 255, 255))
        minus_rect2 = minus_text2.get_rect(center=sfx_minus.center)
        screen.blit(minus_text2, minus_rect2)

        sfx_plus_color = (50, 150, 50) if sfx_plus.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, sfx_plus_color, sfx_plus)
        pygame.draw.rect(screen, (255, 255, 255), sfx_plus, 2)
        plus_text2 = font_settings.render("+", True, (255, 255, 255))
        plus_rect2 = plus_text2.get_rect(center=sfx_plus.center)
        screen.blit(plus_text2, plus_rect2)

        bar_x2 = WIDTH // 2 - 120
        bar_y2 = HEIGHT // 2 + 30
        pygame.draw.rect(screen, (80, 80, 80), (bar_x2, bar_y2, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x2, bar_y2, bar_width * sfx_volume, bar_height))

        circle_x2 = bar_x2 + bar_width * sfx_volume
        pygame.draw.circle(screen, (255, 255, 255), (int(circle_x2), bar_y2 + bar_height // 2), 10)

        if dragging_sfx:
            sfx_volume = max(0, min(1, (mouse_pos[0] - bar_x2) / bar_width))
            set_volumes()

        back_color = (50, 50, 200) if back_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, back_color, back_button)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 3)
        back_text = font_button.render("НАЗАД", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_minus.collidepoint(event.pos):
                    music_volume = max(0, music_volume - 0.1)
                    set_volumes()
                elif music_plus.collidepoint(event.pos):
                    music_volume = min(1, music_volume + 0.1)
                    set_volumes()
                elif sfx_minus.collidepoint(event.pos):
                    sfx_volume = max(0, sfx_volume - 0.1)
                    set_volumes()
                elif sfx_plus.collidepoint(event.pos):
                    sfx_volume = min(1, sfx_volume + 0.1)
                    set_volumes()
                elif back_button.collidepoint(event.pos):
                    return True
                elif bar_x <= event.pos[0] <= bar_x + bar_width and bar_y <= event.pos[1] <= bar_y + bar_height:
                    dragging_music = True
                elif bar_x2 <= event.pos[0] <= bar_x2 + bar_width and bar_y2 <= event.pos[1] <= bar_y2 + bar_height:
                    dragging_sfx = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False
                dragging_sfx = False


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
    play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 70)
    story_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 10, 300, 70)
    settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 70)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 170, 300, 70)

    while True:
        screen.blit(bg_image, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("ASTEROID SHOOTER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        play_color = (50, 50, 200) if play_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, play_color, play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 3)
        play_text = font_button.render("ИГРАТЬ", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_rect)

        story_color = (200, 150, 50) if story_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, story_color, story_button)
        pygame.draw.rect(screen, (255, 255, 255), story_button, 3)
        story_text = font_button.render("СЮЖЕТ", True, (255, 255, 255))
        story_rect = story_text.get_rect(center=story_button.center)
        screen.blit(story_text, story_rect)

        settings_color = (50, 150, 50) if settings_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, settings_color, settings_button)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3)
        settings_text = font_button.render("НАСТРОЙКИ", True, (255, 255, 255))
        settings_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_rect)

        quit_color = (200, 50, 50) if quit_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, quit_color, quit_button)
        pygame.draw.rect(screen, (255, 255, 255), quit_button, 3)
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
                if settings_button.collidepoint(event.pos):
                    if not show_settings():
                        return False
                if quit_button.collidepoint(event.pos):
                    return False


def reset_game():
    global all_sprites, bullets, asteroids, heart_sprites, bosses, boss_bullets
    global powerups, medkits, enemy_planes, laser_bullets, net_bullets
    global diag_bullets, homing_bullets, player_ship, lives, score, medkits_collected
    global boss1_spawned, boss2_spawned, planes_spawned, asteroid_spawn_enabled
    global powerup_active, powerup_end_time, current_shot_delay, next_asteroid_spawn

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

    player_ship = Ship(WIDTH // 2 - 25, HEIGHT - 60)
    all_sprites.add(player_ship)

    lives = 5
    score = 0
    medkits_collected = 0
    boss1_spawned = False
    boss2_spawned = False
    planes_spawned = False
    asteroid_spawn_enabled = True
    powerup_active = False
    powerup_end_time = 0
    current_shot_delay = 0
    next_asteroid_spawn = pygame.time.get_ticks() + 500

    update_hearts()


def update_hearts():
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
last_shot_time = 0
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
                    b = Bullet(player_ship.rect.centerx, player_ship.rect.top)
                    all_sprites.add(b)
                    bullets.add(b)
                    if shoot_sound:
                        shoot_sound.play()
                    last_shot_time = current_time

            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
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
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time >= current_shot_delay:
            b = Bullet(player_ship.rect.centerx, player_ship.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            if shoot_sound:
                shoot_sound.play()
            last_shot_time = current_time

    keys = pygame.key.get_pressed()
    player_ship.update(keys)
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
    for b in bosses:
        if b.update():
            if isinstance(b, GodBoss):
                pattern = b.attack_pattern
                if pattern == 0:
                    lb = LaserBullet(b.rect.centerx, b.rect.bottom)
                    all_sprites.add(lb)
                    laser_bullets.add(lb)
                elif pattern == 1:
                    net = NetBullet(b.rect.centerx, b.rect.bottom)
                    all_sprites.add(net)
                    net_bullets.add(net)
                elif pattern == 2:
                    diag1 = DiagBullet(b.rect.centerx, b.rect.bottom, math.pi/4)
                    diag2 = DiagBullet(b.rect.centerx, b.rect.bottom, -math.pi/4)
                    all_sprites.add(diag1, diag2)
                    diag_bullets.add(diag1, diag2)
                elif pattern == 3:
                    homing = HomingBullet(b.rect.centerx, b.rect.bottom, player_ship)
                    all_sprites.add(homing)
                    homing_bullets.add(homing)
            else:
                bb = BossBullet(b.rect.centerx, b.rect.bottom)
                all_sprites.add(bb)
                boss_bullets.add(bb)

    # Стрельба самолётов
    for plane in enemy_planes:
        if plane.update():
            if isinstance(plane, BluePlane):
                lb = LaserBullet(plane.rect.centerx, plane.rect.bottom)
                all_sprites.add(lb)
                laser_bullets.add(lb)
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
                homing = HomingBullet(plane.rect.centerx, plane.rect.bottom, player_ship)
                all_sprites.add(homing)
                homing_bullets.add(homing)

    # Спавн астероидов
    if asteroid_spawn_enabled and current_time >= next_asteroid_spawn:
        asteroid_type = random.choices([1, 2], weights=[70, 30])[0]
        a = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
        all_sprites.add(a)
        asteroids.add(a)
        next_asteroid_spawn = current_time + random.randint(400, 700)

    # Столкновения пуль с астероидами
    for b in bullets:
        collided = pygame.sprite.spritecollide(b, asteroids, False)
        for a in collided:
            b.kill()
            if a.take_damage():
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
                score += a.points
                drop_chance = 0.3 if a.asteroid_type == 2 else 0.15
                if random.random() < drop_chance:
                    p = PowerUp(a.rect.centerx, a.rect.centery)
                    all_sprites.add(p)
                    powerups.add(p)

                if random.random() < 0.01:
                    m = Medkit(a.rect.centerx, a.rect.centery)
                    all_sprites.add(m)
                    medkits.add(m)

                if a.asteroid_type == 2:
                    pos1_x = max(0, min(a.rect.centerx - 20, WIDTH - 40))
                    pos2_x = max(0, min(a.rect.centerx + 20, WIDTH - 40))
                    small1 = Asteroid(pos1_x, 1, vx=-2)
                    small2 = Asteroid(pos2_x, 1, vx=2)
                    small1.rect.y = a.rect.centery
                    small2.rect.y = a.rect.centery
                    all_sprites.add(small1, small2)
                    asteroids.add(small1, small2)
                a.kill()
            break

    # Столкновения пуль с боссами
    for b in bullets:
        collided = pygame.sprite.spritecollide(b, bosses, False)
        for boss_obj in collided:
            b.kill()
            if boss_obj.take_damage():
                score += boss_obj.points
                if dead_asteroid_sound:
                    transform_sound.play()
                    pygame.mixer.music.play(-1)

                if isinstance(boss_obj, Boss):
                    m = Medkit(boss_obj.rect.centerx, boss_obj.rect.centery)
                    all_sprites.add(m)
                    medkits.add(m)
                    for bb in list(boss_bullets):
                        bb.kill()
                    boss_bullets.empty()
                elif isinstance(boss_obj, GodBoss):
                    for lb in list(laser_bullets):
                        lb.kill()
                    for nb in list(net_bullets):
                        nb.kill()
                    for db in list(diag_bullets):
                        db.kill()
                    for hb in list(homing_bullets):
                        hb.kill()
                    laser_bullets.empty()
                    net_bullets.empty()
                    diag_bullets.empty()
                    homing_bullets.empty()

                if isinstance(boss_obj, GodBoss) and not planes_spawned:
                    planes_spawned = True
                    blue = BluePlane(0, 0)
                    green = GreenPlane(0, 0)
                    red = RedPlane(0, 0)
                    yellow = YellowPlane(0, 0)

                    for plane in [blue, green, red, yellow]:
                        plane.player = player_ship

                    center_x = boss_obj.rect.centerx
                    center_y = boss_obj.rect.centery
                    blue.start_launch(center_x, center_y, -3, -2, 40)
                    green.start_launch(center_x, center_y, 3, -2, 40)
                    red.start_launch(center_x, center_y, -2, 2, 40)
                    yellow.start_launch(center_x, center_y, 2, 2, 40)

                    all_sprites.add(blue, green, red, yellow)
                    enemy_planes.add(blue, green, red, yellow)
            break

    # Столкновения пуль с самолётами
    for b in bullets:
        collided = pygame.sprite.spritecollide(b, enemy_planes, False)
        for plane in collided:
            b.kill()
            if plane.take_damage():
                score += plane.points
                if dead_asteroid_sound:
                    dead_asteroid_sound.play()
            break

    # Столкновения пуль с жёлтыми пулями
    for b in bullets:
        collided = pygame.sprite.spritecollide(b, homing_bullets, True)
        for homing in collided:
            b.kill()
            break

    # Сбор бонусов
    collected = pygame.sprite.spritecollide(player_ship, powerups, True)
    for p in collected:
        if powerup_sound:
            powerup_sound.play()
        powerup_active = True
        powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
        current_shot_delay = SHOT_DELAY_BOOST

    # Сбор аптечек
    collected_medkits = pygame.sprite.spritecollide(player_ship, medkits, True)
    for m in collected_medkits:
        if medkit_sound:
            medkit_sound.play()
        if lives < 5:
            lives = min(lives + 1, 5)
            update_hearts()
            medkits_collected += 1

    # Столкновение с астероидами
    if pygame.sprite.spritecollide(player_ship, asteroids, True):
        if not player_ship.invincible:
            lives -= 1
            player_ship.set_invincible(2000)
            if lives <= 0:
                if boom_sound:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
                    space_pressed = False
                else:
                    running = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

    # Столкновения с пулями боссов
    if pygame.sprite.spritecollide(player_ship, boss_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                last_shot_time = 0
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Столкновения с лазерными пулями
    if pygame.sprite.spritecollide(player_ship, laser_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                last_shot_time = 0
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Столкновения с сетью
    net_hits = pygame.sprite.spritecollide(player_ship, net_bullets, True)
    for net in net_hits:
        player_ship.slow_timer = 180

    # Столкновения с диагональными пулями
    if pygame.sprite.spritecollide(player_ship, diag_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                last_shot_time = 0
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Столкновения с самонаводящимися пулями
    if pygame.sprite.spritecollide(player_ship, homing_bullets, True):
        lives -= 1
        if lives <= 0:
            if boom_sound:
                boom_sound.play()
            pygame.time.wait(500)
            pygame.mixer.music.pause()
            if show_menu():
                reset_game()
                last_shot_time = 0
                space_pressed = False
            else:
                running = False
            pygame.mixer.music.unpause()
        else:
            update_hearts()

    # Спавн первого босса
    if score >= 250 and not boss1_spawned and len(bosses) == 0 and not boss2_spawned:
        boss_obj = Boss(random.randint(100, WIDTH - 100), 50)
        all_sprites.add(boss_obj)
        bosses.add(boss_obj)
        boss1_spawned = True
        spawn_sound.play()
        if dark_sound:
            pygame.mixer.music.stop()
            dark_sound.play(-1)

    # Спавн второго босса
    if score >= 10 and not boss2_spawned and len(bosses) == 0 and not planes_spawned:
        god = GodBoss(random.randint(100, WIDTH - 100), 50)
        all_sprites.add(god)
        bosses.add(god)
        boss2_spawned = True
        asteroid_spawn_enabled = False
        spawn_sound.play()
        if dark_sound:
            pygame.mixer.music.stop()
            dark_sound.play(-1)

    # Возобновление спавна астероидов
    if planes_spawned and len(enemy_planes) == 0 and not asteroid_spawn_enabled:
        asteroid_spawn_enabled = True


    all_sprites.draw(screen)

    # Полоски здоровья
    for boss_obj in bosses:
        max_health = 20 if isinstance(boss_obj, GodBoss) else 10
        health_percent = boss_obj.health / max_health
        bar_width = 200
        bar_height = 15
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 35
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
        boss_text = font.render("БОСС", True, (255, 100, 100))
        screen.blit(boss_text, (WIDTH // 2 - 30, 15))

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
