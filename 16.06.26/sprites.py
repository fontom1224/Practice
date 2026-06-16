import pygame
import random
import math

pygame.init()
pygame.mixer.init()

shoot_sound = pygame.mixer.Sound('assets/OneShoot.mp3')

def safe_load_image(path, default_size=(50, 50)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except (pygame.error, FileNotFoundError):
        print(f"Предупреждение: не удалось загрузить {path}, использую заглушку")
        surf = pygame.Surface(default_size, pygame.SRCALPHA)
        surf.fill((255, 0, 255))
        return surf

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = safe_load_image('assets/ship.png')
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_speed = 5
        self.speed = self.base_speed
        self.slow_timer = 0
        self.slow_factor = 0.5
        self.invincible = False
        self.invincible_end_time = 0

    def set_invincible(self, duration):
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + duration

    def update_invincibility(self):
        if not self.invincible:
            return
        current_time = pygame.time.get_ticks()
        if current_time >= self.invincible_end_time:
            self.invincible = False
            self.image = self.base_image.copy()
        else:
            alpha = 128 if (current_time // 100) % 2 == 0 else 255
            self.image = self.base_image.copy()
            self.image.set_alpha(alpha)

    def update(self, keys):
        self.update_invincibility()
        if self.slow_timer > 0:
            self.slow_timer -= 1
            self.speed = self.base_speed * self.slow_factor
        else:
            self.speed = self.base_speed

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -7
        self.damage = 1   # обычный урон

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# ----- УСИЛЕННАЯ ПУЛЯ (тройной урон) -----
class PowerBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage = 3
        try:
            self.image = pygame.image.load('assets/powerbullet.png').convert_alpha()
        except:
            self.image = pygame.Surface((12, 24), pygame.SRCALPHA)
            self.image.fill((255, 255, 0))
            pygame.draw.rect(self.image, (255, 200, 0), self.image.get_rect(), 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# ----- АСТЕРОИДЫ -----
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, asteroid_type=1, vx=0):
        super().__init__()
        self.vx = vx
        if asteroid_type == 1:
            self.image_path = 'assets/asteroid1.png'
            self.size_factor = 1.3
            self.health = 1
            self.speed = 4
            self.points = 10
        else:
            self.image_path = 'assets/asteroid2.png'
            self.size_factor = 1.1
            self.health = 3
            self.speed = 2
            self.points = 30

        original_image = safe_load_image(self.image_path)
        width = int(original_image.get_width() * self.size_factor)
        height = int(original_image.get_height() * self.size_factor)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -40
        self.asteroid_type = asteroid_type

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.speed
        if (self.rect.top > 600 or self.rect.bottom < 0 or
            self.rect.right < 0 or self.rect.left > 800):
            self.kill()

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0

# ----- СЕРДЕЧКИ (жизни) -----
class Hp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/HealthsWhiteBorder.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# ----- ПУЛИ БОССОВ -----
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/bossbullet.png')
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# ----- ПЕРВЫЙ БОСС -----
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/boss.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.health = 10
        self.points = 100
        self.direction = 1
        self.change_direction_timer = 0
        self.direction_interval = random.randint(60, 180)
        self.shoot_timer = 0
        self.shoot_delay = 45

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > 800:
            self.rect.right = 800
            self.direction = -1

        self.change_direction_timer += 1
        if self.change_direction_timer >= self.direction_interval:
            self.direction *= -1
            self.change_direction_timer = 0
            self.direction_interval = random.randint(60, 180)

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            if shoot_sound:
                shoot_sound.play()
            return True
        return False

    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

# ----- АПТЕЧКА -----
class Medkit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/medkit.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# ----- БОНУС УСКОРЕНИЯ -----
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/speedUpg.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# ----- БОГ-АСТЕРОИД (второй босс) -----
class GodBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/god.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 20
        self.points = 200
        self.homing_chance = 0.05

        self.direction = 1
        self.change_dir_timer = 0
        self.dir_interval = random.randint(60, 180)

        self.shoot_timer = 0
        self.shoot_delay = 30
        self.attack_pattern = 0
        self.pattern_change_timer = 0
        self.pattern_interval = 120

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > 800:
            self.rect.right = 800
            self.direction = -1

        self.change_dir_timer += 1
        if self.change_dir_timer >= self.dir_interval:
            self.direction *= -1
            self.change_dir_timer = 0
            self.dir_interval = random.randint(60, 180)

        self.pattern_change_timer += 1
        if self.pattern_change_timer >= self.pattern_interval:
            self.pattern_change_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 4

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            if self.attack_pattern == 3 and random.random() < self.homing_chance:
                return False
            return True
        return False

    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

# ----- ТИПЫ ПУЛЬ ДЛЯ БОССОВ И САМОЛЁТОВ -----
class LaserBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/bluebullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class NetBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = safe_load_image('assets/greenbullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class DiagBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = safe_load_image('assets/redbullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5
        self.dx = math.sin(angle) * self.speed
        self.dy = math.cos(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.top > 600 or self.rect.bottom < 0 or
            self.rect.left < 0 or self.rect.right > 800):
            self.kill()

class HomingBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = safe_load_image('assets/yellowbullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 1.5
        self.target = target

    def update(self):
        if self.target is None or not self.target.alive():
            self.kill()
            return
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
        if (self.rect.top > 600 or self.rect.bottom < 0 or
            self.rect.left < 0 or self.rect.right > 800):
            self.kill()

# ----- САМОЛЁТЫ (миньоны) -----
class EnemyPlaneBase(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, shoot_delay=60, move_speed=2):
        super().__init__()
        self.image = safe_load_image(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3
        self.points = 20
        self.shoot_timer = 0
        self.shoot_delay = 60
        self.player = None
        self.move_speed = move_speed
        self.direction = 1

        self.launch_mode = False
        self.launch_vx = 0
        self.launch_vy = 0
        self.launch_timer = 0

        self.shots_per_burst = 3
        self.shots_done = 0
        self.burst_pause = 180
        self.pause_timer = 0

    def start_launch(self, start_x, start_y, vx, vy, duration=40):
        self.rect.centerx = start_x
        self.rect.centery = start_y
        self.launch_mode = True
        self.launch_vx = vx
        self.launch_vy = vy
        self.launch_timer = duration

    def update(self):
        if self.launch_mode:
            self.rect.x += self.launch_vx
            self.rect.y += self.launch_vy
            self.launch_timer -= 1
            if self.launch_timer <= 0:
                self.launch_mode = False
            return False

        self.rect.x += self.move_speed * self.direction
        if self.rect.right >= 800:
            self.rect.right = 800
            self.direction = -1
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1

        if self.rect.top > 600 or self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > 800:
            self.kill()
            return False

        if self.pause_timer > 0:
            self.pause_timer -= 1
            return False

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shots_done += 1
            if self.shots_done >= self.shots_per_burst:
                self.shots_done = 0
                self.pause_timer = self.burst_pause
            return True
        return False

    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

class BluePlane(EnemyPlaneBase):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/blue.png', shoot_delay=100, move_speed=2)

class GreenPlane(EnemyPlaneBase):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/green.png', shoot_delay=60, move_speed=2)

class RedPlane(EnemyPlaneBase):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/red.png', shoot_delay=90, move_speed=2)

class YellowPlane(EnemyPlaneBase):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/yellow.png', shoot_delay=120, move_speed=2)

# ----- ТРЕТИЙ БОСС (финальный) -----
class ThirdBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = safe_load_image('assets/avenger.png')
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.base_speed = 2
        self.speed = self.base_speed
        self.health = 50
        self.points = 300
        
        self.direction = 1
        self.change_dir_timer = 0
        self.dir_interval = random.randint(80, 150)

        self.pattern = 0
        self.pattern_timer = 0
        self.pattern_interval = 150
        self.shoot_timer = 0
        self.base_shoot_delay = 40
        self.shoot_delay = self.base_shoot_delay

        self.y_speed = 1
        self.y_direction = 1
        self.start_y = y
        self.y_range = 40

        self.phase2 = False
        self.alpha = 255
        self.alpha_change = -3
        self.spiral_angle = 0

    def update(self, player=None):
        if self.phase2 and player is not None:
            self.speed = self.base_speed * 1.4
            if self.rect.centerx < player.rect.centerx - 20:
                self.rect.x += self.speed
            elif self.rect.centerx > player.rect.centerx + 20:
                self.rect.x -= self.speed
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.left < 0:
                self.rect.left = 0
                self.direction = 1
            if self.rect.right > 800:
                self.rect.right = 800
                self.direction = -1

            self.change_dir_timer += 1
            if self.change_dir_timer >= self.dir_interval:
                self.direction *= -1
                self.change_dir_timer = 0
                self.dir_interval = random.randint(80, 150)

        current_y_speed = self.y_speed * 1.5 if self.phase2 else self.y_speed
        self.rect.y += current_y_speed * self.y_direction
        y_range = 60 if self.phase2 else self.y_range
        
        if (self.rect.y < self.start_y - y_range or 
            self.rect.y > self.start_y + y_range):
            self.y_direction *= -1

        if self.health <= 25 and not self.phase2:
            self.phase2 = True
            self.pattern_interval = 80
            self.base_shoot_delay = 25
            self.shoot_delay = self.base_shoot_delay

        if self.phase2:
            self.alpha += self.alpha_change
            if self.alpha <= 100 or self.alpha >= 255:
                self.alpha_change *= -1
                self.alpha = max(100, min(255, self.alpha))
            self.image = self.original_image.copy()
            self.image.set_alpha(int(self.alpha))
        else:
            self.image = self.original_image.copy()
            self.image.set_alpha(255)

        self.pattern_timer += 1
        if self.pattern_timer >= self.pattern_interval:
            self.pattern_timer = 0
            if self.phase2:
                self.pattern = (self.pattern + 1) % 5
            else:
                self.pattern = (self.pattern + 1) % 4

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False

    def fire(self, player):
        bullets = []
        x, y = self.rect.centerx, self.rect.bottom

        def add_homing(count=1):
            for _ in range(count):
                offset = random.randint(-15, 15)
                bullets.append(HomingBullet(x + offset, y, player))

        if not self.phase2:
            if self.pattern == 0:
                dx = player.rect.centerx - x
                dy = player.rect.centery - y
                base_angle = math.atan2(dx, dy)
                for offset in [-0.15, 0, 0.15]:
                    bullets.append(DiagBullet(x, y, base_angle + offset))
            elif self.pattern == 1:
                for i in range(-2, 3):
                    angle = math.radians(i * 20)
                    bullets.append(DiagBullet(x, y, angle))
            elif self.pattern == 2:
                bullets.append(LaserBullet(150, y))
                bullets.append(LaserBullet(650, y))
                bullets.append(BossBullet(x - 30, y))
                bullets.append(BossBullet(x + 30, y))
            elif self.pattern == 3:
                add_homing(2)
        else:
            if self.pattern == 0:
                self.spiral_angle = (self.spiral_angle + 15) % 360
                for i in range(8):
                    angle = math.radians(self.spiral_angle + i * 45)
                    bullets.append(DiagBullet(x, y, angle))
            elif self.pattern == 1:
                bullets.append(NetBullet(x - 180, y))
                bullets.append(NetBullet(x + 180, y))
                bullets.append(LaserBullet(x, y))
                add_homing(1)
            elif self.pattern == 2:
                dx = player.rect.centerx - x
                dy = player.rect.centery - y
                base_angle = math.atan2(dx, dy)
                for offset in [-0.1, 0, 0.1]:
                    b = DiagBullet(x, y, base_angle + offset)
                    b.speed = 7
                    bullets.append(b)
            elif self.pattern == 3:
                for i in range(5):
                    bullets.append(DiagBullet(x - 50, y, math.radians(45)))
                    bullets.append(DiagBullet(x + 50, y, math.radians(-45)))
            elif self.pattern == 4:
                for i in range(-4, 5):
                    angle = math.radians(i * 18)
                    bullets.append(DiagBullet(x, y, angle))
                add_homing(1)

        return bullets

    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False
