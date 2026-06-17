import pygame
import random
import math
import sys
import os
import sprites
from sprites import *

# ---------- Функция для корректного пути к ресурсам ----------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------------------------------------------------

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()
bg_original = pygame.image.load(resource_path('assets/fon.png'))
bg_image = pygame.transform.scale(bg_original, (800, 600))

# Шрифты
font_title = pygame.font.Font(None, 72)
font_button = pygame.font.Font(None, 48)
font_settings = pygame.font.Font(None, 36)
font_pause = pygame.font.Font(None, 60)

# Настройки звука
music_volume = 1.0
sfx_volume = 1.0

# ===== СЛОЖНОСТЬ (только для отображения) =====
difficulty = "Средняя"

# ===== ЗВУКИ =====
boom_sound = None
dead_asteroid_sound = None
shoot_sound = None
powerup_sound = None
medkit_sound = None
dark_sound = None
spawn_sound = None
transform_sound = None

try:
    boom_sound = pygame.mixer.Sound(resource_path('assets/Boom.mp3'))
    dead_asteroid_sound = pygame.mixer.Sound(resource_path('assets/DeadAsteroid.mp3'))
    shoot_sound = pygame.mixer.Sound(resource_path('assets/OneShoot.mp3'))
    powerup_sound = pygame.mixer.Sound(resource_path('assets/PowerUp.mp3'))
    medkit_sound = pygame.mixer.Sound(resource_path('assets/Medkit.mp3'))
    dark_sound = pygame.mixer.Sound(resource_path('assets/DarkSouls.mp3'))
    spawn_sound = pygame.mixer.Sound(resource_path('assets/terraria.mp3'))
    transform_sound = pygame.mixer.Sound(resource_path('assets/transform.mp3'))

    shoot_sound.set_volume(0.3)
    medkit_sound.set_volume(1)
    spawn_sound.set_volume(1)
    dark_sound.set_volume(0.2)

    pygame.mixer.music.load(resource_path('assets/Music.mp3'))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except FileNotFoundError as e:
    print(f"Ошибка: не найден звуковой файл - {e}")

# ----- Устанавливаем глобальные звуки в модуле sprites -----
sprites.shoot_sound = shoot_sound

# ===== ПОПАПЫ =====
popup_queue = []
popup_active = False
popup_text = ""
popup_start_time = 0
popup_duration = 3000

try:
    face_img = pygame.image.load(resource_path('assets/face.png')).convert_alpha()
except FileNotFoundError:
    face_img = pygame.Surface((60, 60))
    face_img.fill((200, 100, 50))
    pygame.draw.circle(face_img, (255, 255, 255), (30, 25), 15)
    pygame.draw.circle(face_img, (0, 0, 0), (20, 20), 3)
    pygame.draw.circle(face_img, (0, 0, 0), (40, 20), 3)
    pygame.draw.arc(face_img, (0, 0, 0), (15, 30, 30, 15), 0, math.pi, 2)

def show_popup(text, duration=3000):
    global popup_queue, popup_active
    popup_queue.append((text, duration))
    if not popup_active:
        show_next_popup()

def show_next_popup():
    global popup_active, popup_text, popup_start_time, popup_duration, popup_queue
    if popup_queue:
        text, duration = popup_queue.pop(0)
        popup_active = True
        popup_text = text
        popup_start_time = pygame.time.get_ticks()
        popup_duration = duration
    else:
        popup_active = False

# ===== ГРОМКОСТЬ =====
def set_volumes():
    pygame.mixer.music.set_volume(music_volume)
    if dark_sound is not None:
        dark_sound.set_volume(music_volume)
    if boom_sound is not None:
        boom_sound.set_volume(sfx_volume)
    if dead_asteroid_sound is not None:
        dead_asteroid_sound.set_volume(sfx_volume)
    if shoot_sound is not None:
        shoot_sound.set_volume(sfx_volume)
    if powerup_sound is not None:
        powerup_sound.set_volume(sfx_volume)
    if medkit_sound is not None:
        medkit_sound.set_volume(sfx_volume)
    if transform_sound is not None:
        transform_sound.set_volume(sfx_volume)

# ===== МЕНЮ НАСТРОЕК =====
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

# ===== СЮЖЕТ =====
def show_story():
    story_images = []
    for i in range(1, 5):
        try:
            img = pygame.image.load(resource_path(f'assets/frame{i}.png')).convert_alpha()
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

# ===== МЕНЮ СЛОЖНОСТИ =====
def show_difficulty_menu():
    global difficulty

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))

    easy_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 60)
    medium_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
    hard_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 60)
    back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50)

    while True:
        screen.blit(overlay, (0, 0))

        title = font_title.render("ВЫБОР СЛОЖНОСТИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        color = (50, 200, 50) if easy_btn.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(screen, color, easy_btn)
        pygame.draw.rect(screen, (255, 255, 255), easy_btn, 2)
        text = font_button.render("ЛЁГКАЯ", True, (255, 255, 255))
        text_rect = text.get_rect(center=easy_btn.center)
        screen.blit(text, text_rect)

        color = (200, 200, 50) if medium_btn.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(screen, color, medium_btn)
        pygame.draw.rect(screen, (255, 255, 255), medium_btn, 2)
        text = font_button.render("СРЕДНЯЯ", True, (255, 255, 255))
        text_rect = text.get_rect(center=medium_btn.center)
        screen.blit(text, text_rect)

        color = (200, 50, 50) if hard_btn.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(screen, color, hard_btn)
        pygame.draw.rect(screen, (255, 255, 255), hard_btn, 2)
        text = font_button.render("СЛОЖНАЯ", True, (255, 255, 255))
        text_rect = text.get_rect(center=hard_btn.center)
        screen.blit(text, text_rect)

        color = (100, 100, 200) if back_btn.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, color, back_btn)
        pygame.draw.rect(screen, (255, 255, 255), back_btn, 2)
        text = font_button.render("НАЗАД", True, (255, 255, 255))
        text_rect = text.get_rect(center=back_btn.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    difficulty = "Лёгкая"
                    return
                if medium_btn.collidepoint(event.pos):
                    difficulty = "Средняя"
                    return
                if hard_btn.collidepoint(event.pos):
                    difficulty = "Сложная"
                    return
                if back_btn.collidepoint(event.pos):
                    return

# ===== ГЛАВНОЕ МЕНЮ =====
def show_menu():
    play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 70)
    skull_button = pygame.Rect(WIDTH // 2 + 160, HEIGHT // 2 - 100, 70, 70)

    story_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 10, 300, 70)
    settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 70)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 170, 300, 70)

    skull_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    skull_surf.fill((0, 0, 0, 0))
    font_skull = pygame.font.Font(None, 60)
    text = font_skull.render(':)', True, (255, 255, 255))
    text_rect = text.get_rect(center=(30, 30))
    skull_surf.blit(text, text_rect)
    skull_img = skull_surf

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

        # ИГРАТЬ
        color = (50, 50, 200) if play_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 3)
        play_text = font_button.render("ИГРАТЬ", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_rect)

        # Смайлик (сложность)
        color = (150, 150, 150) if skull_button.collidepoint(mouse_pos) else (80, 80, 80)
        pygame.draw.rect(screen, color, skull_button)
        pygame.draw.rect(screen, (255, 255, 255), skull_button, 3)
        skull_rect = skull_img.get_rect(center=skull_button.center)
        screen.blit(skull_img, skull_rect)

        # СЮЖЕТ
        color = (200, 150, 50) if story_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, story_button)
        pygame.draw.rect(screen, (255, 255, 255), story_button, 3)
        story_text = font_button.render("СЮЖЕТ", True, (255, 255, 255))
        story_rect = story_text.get_rect(center=story_button.center)
        screen.blit(story_text, story_rect)

        # НАСТРОЙКИ
        color = (50, 150, 50) if settings_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, settings_button)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3)
        settings_text = font_button.render("НАСТРОЙКИ", True, (255, 255, 255))
        settings_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_rect)

        # ВЫХОД
        color = (200, 50, 50) if quit_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, quit_button)
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
                if skull_button.collidepoint(event.pos):
                    show_difficulty_menu()
                if story_button.collidepoint(event.pos):
                    show_story()
                if settings_button.collidepoint(event.pos):
                    if not show_settings():
                        return False
                if quit_button.collidepoint(event.pos):
                    return False

# ===== МЕНЮ ПАУЗЫ =====
def show_pause_menu():
    pause_overlay = pygame.Surface((WIDTH, HEIGHT))
    pause_overlay.set_alpha(180)
    pause_overlay.fill((0, 0, 0))

    continue_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 70)
    settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 10, 300, 70)
    menu_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 70)

    while True:
        screen.blit(pause_overlay, (0, 0))
        title = font_pause.render("ПАУЗА", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 170))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        color = (50, 200, 50) if continue_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, continue_button)
        pygame.draw.rect(screen, (255, 255, 255), continue_button, 3)
        text = font_button.render("ПРОДОЛЖИТЬ", True, (255, 255, 255))
        text_rect = text.get_rect(center=continue_button.center)
        screen.blit(text, text_rect)

        color = (50, 50, 200) if settings_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, settings_button)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3)
        text = font_button.render("НАСТРОЙКИ", True, (255, 255, 255))
        text_rect = text.get_rect(center=settings_button.center)
        screen.blit(text, text_rect)

        color = (200, 50, 50) if menu_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, menu_button)
        pygame.draw.rect(screen, (255, 255, 255), menu_button, 3)
        text = font_button.render("ВЫЙТИ В МЕНЮ", True, (255, 255, 255))
        text_rect = text.get_rect(center=menu_button.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return True
                if settings_button.collidepoint(event.pos):
                    show_settings()
                if menu_button.collidepoint(event.pos):
                    return False

# ===== СБРОС ИГРЫ =====
def reset_game():
    global all_sprites, bullets, asteroids, heart_sprites, bosses, boss_bullets
    global powerups, medkits, enemy_planes, laser_bullets, net_bullets
    global diag_bullets, homing_bullets, player_ship, lives, score
    global boss1_spawned, boss2_spawned, planes_spawned, asteroid_spawn_enabled, boss3_spawned
    global powerup_active, powerup_end_time, current_shot_delay, next_asteroid_spawn
    global power_shots, next_power_shot_threshold, first_power_shot_shown
    global popup_queue, popup_active

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
    boss1_spawned = False
    boss2_spawned = False
    boss3_spawned = False
    planes_spawned = False
    asteroid_spawn_enabled = True
    powerup_active = False
    powerup_end_time = 0
    current_shot_delay = 400
    next_asteroid_spawn = pygame.time.get_ticks() + 500

    # Усиленные патроны
    power_shots = 0
    next_power_shot_threshold = 150
    first_power_shot_shown = False

    # Попапы
    popup_queue = []
    popup_active = False
    show_popup("Ты, должно быть, новенький?\nПозволь провести тебя!", duration=3000)
    show_popup("Для движения используй стрелочки,\nчтобы выстрелить — нажми ПРОБЕЛ.\nЯ в тебя верю :D", duration=4000)

    update_hearts()

def update_hearts():
    for heart in heart_sprites:
        heart.kill()
    heart_sprites.empty()
    for i in range(lives):
        heart = Hp(10 + i * 40, 10)
        heart_sprites.add(heart)
        all_sprites.add(heart)

# ==================== ОСНОВНОЙ ЦИКЛ ====================
game_active = True
while game_active:
    if not show_menu():
        game_active = False
        break

    reset_game()

    BASE_SHOT_DELAY = 400
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
                game_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time >= current_shot_delay:
                        b = Bullet(player_ship.rect.centerx, player_ship.rect.top)
                        all_sprites.add(b)
                        bullets.add(b)
                        if shoot_sound is not None:
                            shoot_sound.play()
                        last_shot_time = current_time

                # Усиленный выстрел
                if event.key == pygame.K_x and power_shots > 0:
                    pb = PowerBullet(player_ship.rect.centerx, player_ship.rect.top)
                    all_sprites.add(pb)
                    bullets.add(pb)
                    power_shots -= 1
                    if shoot_sound is not None:
                        shoot_sound.play()

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    continue_game = show_pause_menu()
                    pygame.mixer.music.unpause()
                    if not continue_game:
                        running = False
                        pygame.mixer.music.stop()
                        break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False

        if not running:
            continue

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
                if shoot_sound is not None:
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

        # ===== СТРЕЛЬБА БОССОВ =====
        for b in bosses:
            if b.update():
                if isinstance(b, ThirdBoss):
                    new_bullets = b.fire(player_ship)
                    for bullet in new_bullets:
                        all_sprites.add(bullet)
                        if isinstance(bullet, LaserBullet):
                            laser_bullets.add(bullet)
                        elif isinstance(bullet, BossBullet):
                            boss_bullets.add(bullet)
                        elif isinstance(bullet, DiagBullet):
                            diag_bullets.add(bullet)
                        elif isinstance(bullet, HomingBullet):
                            homing_bullets.add(bullet)
                        elif isinstance(bullet, NetBullet):
                            net_bullets.add(bullet)
                elif isinstance(b, GodBoss):
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
                        diag1 = DiagBullet(b.rect.centerx, b.rect.bottom, math.pi / 4)
                        diag2 = DiagBullet(b.rect.centerx, b.rect.bottom, -math.pi / 4)
                        all_sprites.add(diag1, diag2)
                        diag_bullets.add(diag1, diag2)
                    elif pattern == 3:
                        homing = HomingBullet(b.rect.centerx, b.rect.bottom, player_ship)
                        all_sprites.add(homing)
                        homing_bullets.add(homing)
                elif isinstance(b, Boss):
                    bb = BossBullet(b.rect.centerx, b.rect.bottom)
                    all_sprites.add(bb)
                    boss_bullets.add(bb)

        # ===== СТРЕЛЬБА САМОЛЁТОВ =====
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
                    diag1 = DiagBullet(plane.rect.centerx, plane.rect.bottom, math.pi / 4)
                    diag2 = DiagBullet(plane.rect.centerx, plane.rect.bottom, -math.pi / 4)
                    all_sprites.add(diag1, diag2)
                    diag_bullets.add(diag1, diag2)
                elif isinstance(plane, YellowPlane):
                    homing = HomingBullet(plane.rect.centerx, plane.rect.bottom, player_ship)
                    all_sprites.add(homing)
                    homing_bullets.add(homing)

        # ===== СПАВН АСТЕРОИДОВ =====
        if asteroid_spawn_enabled and current_time >= next_asteroid_spawn:
            asteroid_type = random.choices([1, 2], weights=[70, 30])[0]
            a = Asteroid(random.randint(0, WIDTH - 40), asteroid_type)
            all_sprites.add(a)
            asteroids.add(a)
            next_asteroid_spawn = current_time + random.randint(400, 700)

        # ===== СТОЛКНОВЕНИЯ ПУЛЬ С АСТЕРОИДАМИ =====
        for b in bullets:
            collided = pygame.sprite.spritecollide(b, asteroids, False)
            for a in collided:
                b.kill()
                if a.take_damage(b.damage):
                    if dead_asteroid_sound is not None:
                        dead_asteroid_sound.play()
                    score += a.points

                    # Выдача усиленных патронов
                    while score >= next_power_shot_threshold:
                        power_shots += 1
                        if not first_power_shot_shown:
                            first_power_shot_shown = True
                            show_popup("Ты получил усиленный патрон!\nНажми X, чтобы его выпустить\nОн наносит тройной урон!", duration=4000)
                        next_power_shot_threshold += 150

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

        # ===== СТОЛКНОВЕНИЯ ПУЛЬ С БОССАМИ =====
        for b in bullets:
            collided = pygame.sprite.spritecollide(b, bosses, False)
            for boss_obj in collided:
                b.kill()
                if boss_obj.take_damage(b.damage):
                    score += boss_obj.points

                    # Выдача усиленных патронов
                    while score >= next_power_shot_threshold:
                        power_shots += 1
                        if not first_power_shot_shown:
                            first_power_shot_shown = True
                            show_popup("Ты получил усиленный патрон!\nНажми X, чтобы его выпустить\nОн наносит тройной урон!", duration=4000)
                        next_power_shot_threshold += 150

                    if isinstance(boss_obj, Boss):
                        asteroid_spawn_enabled = True
                        m = Medkit(boss_obj.rect.centerx, boss_obj.rect.centery)
                        all_sprites.add(m)
                        medkits.add(m)
                        for bb in list(boss_bullets):
                            bb.kill()
                        boss_bullets.empty()
                        if dark_sound is not None:
                            dark_sound.stop()
                        pygame.mixer.music.load(resource_path('assets/Music.mp3'))
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
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
                        if dark_sound is not None:
                            dark_sound.stop()
                        pygame.mixer.music.load(resource_path('assets/Music.mp3'))
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                    elif isinstance(boss_obj, ThirdBoss):
                        asteroid_spawn_enabled = True
                        m = Medkit(boss_obj.rect.centerx, boss_obj.rect.centery)
                        all_sprites.add(m)
                        medkits.add(m)
                        for lb in list(laser_bullets):
                            lb.kill()
                        for db in list(diag_bullets):
                            db.kill()
                        for bb in list(boss_bullets):
                            bb.kill()
                        for hb in list(homing_bullets):
                            hb.kill()
                        laser_bullets.empty()
                        diag_bullets.empty()
                        boss_bullets.empty()
                        homing_bullets.empty()
                        if dark_sound is not None:
                            dark_sound.stop()
                        pygame.mixer.music.load(resource_path('assets/Music.mp3'))
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)

                    if isinstance(boss_obj, GodBoss) and not planes_spawned:
                        if transform_sound is not None:
                            transform_sound.play()
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

        # ===== СТОЛКНОВЕНИЯ ПУЛЬ С САМОЛЁТАМИ =====
        for b in bullets:
            collided = pygame.sprite.spritecollide(b, enemy_planes, False)
            for plane in collided:
                b.kill()
                if plane.take_damage(b.damage):
                    score += plane.points

                    # Выдача усиленных патронов
                    while score >= next_power_shot_threshold:
                        power_shots += 1
                        if not first_power_shot_shown:
                            first_power_shot_shown = True
                            show_popup("Ты получил усиленный патрон!\nНажми X, чтобы его выпустить\nОн наносит тройной урон!", duration=4000)
                        next_power_shot_threshold += 150

                    if dead_asteroid_sound is not None:
                        dead_asteroid_sound.play()
                break

        # ===== СТОЛКНОВЕНИЯ ПУЛЬ С ЖЁЛТЫМИ ПУЛЯМИ =====
        for b in bullets:
            collided = pygame.sprite.spritecollide(b, homing_bullets, True)
            for homing in collided:
                b.kill()
                break

        # ===== СБОР БОНУСОВ =====
        collected = pygame.sprite.spritecollide(player_ship, powerups, True)
        for p in collected:
            if powerup_sound is not None:
                powerup_sound.play()
            powerup_active = True
            powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
            current_shot_delay = SHOT_DELAY_BOOST

        # ===== СБОР АПТЕЧЕК =====
        collected_medkits = pygame.sprite.spritecollide(player_ship, medkits, True)
        for m in collected_medkits:
            if medkit_sound is not None:
                medkit_sound.play()
            if lives < 5:
                lives = min(lives + 1, 5)
                update_hearts()

        # ===== СТОЛКНОВЕНИЕ С АСТЕРОИДАМИ =====
        if pygame.sprite.spritecollide(player_ship, asteroids, True):
            if not player_ship.invincible:
                lives -= 1
                player_ship.set_invincible(2000)
                if lives <= 0:
                    if boom_sound is not None:
                        boom_sound.play()
                    pygame.time.wait(500)
                    pygame.mixer.music.pause()
                    if show_menu():
                        reset_game()
                        last_shot_time = 0
                        space_pressed = False
                        continue
                    else:
                        running = False
                        game_active = False
                    pygame.mixer.music.unpause()
                else:
                    update_hearts()

        # ===== СТОЛКНОВЕНИЯ С ПУЛЯМИ БОССОВ =====
        if pygame.sprite.spritecollide(player_ship, boss_bullets, True):
            lives -= 1
            if lives <= 0:
                if boom_sound is not None:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
                    space_pressed = False
                    continue
                else:
                    running = False
                    game_active = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

        # ===== СТОЛКНОВЕНИЯ С ЛАЗЕРНЫМИ ПУЛЯМИ =====
        if pygame.sprite.spritecollide(player_ship, laser_bullets, True):
            lives -= 1
            if lives <= 0:
                if boom_sound is not None:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
                    space_pressed = False
                    continue
                else:
                    running = False
                    game_active = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

        # ===== СТОЛКНОВЕНИЯ С СЕТЬЮ =====
        net_hits = pygame.sprite.spritecollide(player_ship, net_bullets, True)
        for net in net_hits:
            player_ship.slow_timer = 180

        # ===== СТОЛКНОВЕНИЯ С ДИАГОНАЛЬНЫМИ ПУЛЯМИ =====
        if pygame.sprite.spritecollide(player_ship, diag_bullets, True):
            lives -= 1
            if lives <= 0:
                if boom_sound is not None:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
                    space_pressed = False
                    continue
                else:
                    running = False
                    game_active = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

        # ===== СТОЛКНОВЕНИЯ С САМОНАВОДЯЩИМИСЯ ПУЛЯМИ =====
        if pygame.sprite.spritecollide(player_ship, homing_bullets, True):
            lives -= 1
            if lives <= 0:
                if boom_sound is not None:
                    boom_sound.play()
                pygame.time.wait(500)
                pygame.mixer.music.pause()
                if show_menu():
                    reset_game()
                    last_shot_time = 0
                    space_pressed = False
                    continue
                else:
                    running = False
                    game_active = False
                pygame.mixer.music.unpause()
            else:
                update_hearts()

        # ===== СТОЛКНОВЕНИЕ С БОССАМИ (отталкивание) =====
        for boss_obj in bosses:
            if pygame.sprite.collide_rect(player_ship, boss_obj):
                if not player_ship.invincible:
                    lives -= 1
                    player_ship.set_invincible(2000)
                    if lives <= 0:
                        if boom_sound is not None:
                            boom_sound.play()
                        pygame.time.wait(500)
                        pygame.mixer.music.pause()
                        if show_menu():
                            reset_game()
                            last_shot_time = 0
                            space_pressed = False
                            continue
                        else:
                            running = False
                            game_active = False
                        pygame.mixer.music.unpause()
                    else:
                        update_hearts()
                    # Отталкиваем игрока
                    if player_ship.rect.centery < boss_obj.rect.centery:
                        player_ship.rect.y -= 15
                    else:
                        player_ship.rect.y += 15

        # ===== СПАВН БОССОВ =====
        if score >= 250 and not boss1_spawned and len(bosses) == 0 and not boss2_spawned:
            boss_obj = Boss(random.randint(100, WIDTH - 100), 50)
            all_sprites.add(boss_obj)
            bosses.add(boss_obj)
            boss1_spawned = True
            asteroid_spawn_enabled = False
            if spawn_sound is not None:
                spawn_sound.play()
            if dark_sound is not None:
                pygame.mixer.music.stop()
                dark_sound.play(-1)
            show_popup("Опа\nЭто твой первый босс", duration=2500)

        if score >= 750 and not boss2_spawned and len(bosses) == 0 and not planes_spawned:
            god = GodBoss(random.randint(100, WIDTH - 100), 50)
            all_sprites.add(god)
            bosses.add(god)
            boss2_spawned = True
            asteroid_spawn_enabled = False
            if spawn_sound is not None:
                spawn_sound.play()
            if dark_sound is not None:
                pygame.mixer.music.stop()
                dark_sound.play(-1)
            show_popup("Это Бог-Астероид!\nПриготовься, у него миньоны!", duration=2500)

        if score >= 1500 and not boss3_spawned and len(bosses) == 0:
            third = ThirdBoss(random.randint(100, WIDTH - 100), 50)
            all_sprites.add(third)
            bosses.add(third)
            boss3_spawned = True
            asteroid_spawn_enabled = False
            if dark_sound is not None:
                pygame.mixer.music.stop()
                dark_sound.play(-1)
            show_popup("Финал близок\nЭто последний бой", duration=2500)

        if planes_spawned and len(enemy_planes) == 0 and not asteroid_spawn_enabled:
            asteroid_spawn_enabled = True

        # ===== ОТРИСОВКА =====
        all_sprites.draw(screen)

        # Полоски здоровья боссов
        for boss_obj in bosses:
            if isinstance(boss_obj, ThirdBoss):
                max_health = 50
            elif isinstance(boss_obj, GodBoss):
                max_health = 20
            else:
                max_health = 10
            health_percent = boss_obj.health / max_health
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

        # Счёт и усиленные патроны
        score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 50))
        power_text = font.render(f"Усиленные: {power_shots}", True, (255, 255, 255))
        screen.blit(power_text, (10, 90))

        # Индикатор ускорения
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

        # Попап
        if popup_active:
            elapsed = pygame.time.get_ticks() - popup_start_time
            if elapsed >= popup_duration:
                show_next_popup()
            else:
                popup_surf = pygame.Surface((400, 130), pygame.SRCALPHA)
                popup_surf.fill((0, 0, 0, 200))
                pygame.draw.rect(popup_surf, (255, 255, 255), popup_surf.get_rect(), 2)
                if face_img is not None:
                    face_scaled = pygame.transform.scale(face_img, (60, 60))
                    popup_surf.blit(face_scaled, (10, 20))
                font_popup = pygame.font.Font(None, 24)
                lines = popup_text.split('\n')
                y = 15
                for line in lines:
                    text_surf = font_popup.render(line, True, (255, 255, 255))
                    popup_surf.blit(text_surf, (80, y))
                    y += 26
                screen.blit(popup_surf, (10, HEIGHT - 150))

        pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
