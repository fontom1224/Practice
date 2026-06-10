import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/ship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, asteroid_type=1):
        super().__init__()

        # Базовые параметры по типам
        if asteroid_type == 1:  # Маленький метеор
            self.image_path = 'images/asteroid1.png'
            self.size_factor = 0.7  # 70% от оригинала
            self.health = 1  # Уничтожается одной пулей
            self.speed = 4
        else:  # asteroid_type == 2 — Большой метеор
            self.image_path = 'images/asteroid2.png'
            self.size_factor = 1.5  # 150% от оригинала
            self.health = 3  # Нужно 3 пули
            self.speed = 2

        # Загружаем и масштабируем изображение
        original_image = pygame.image.load(self.image_path).convert_alpha()
        width = int(original_image.get_width() * self.size_factor)
        height = int(original_image.get_height() * self.size_factor)
        self.image = pygame.transform.scale(original_image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -40
        self.asteroid_type = asteroid_type

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

    def take_damage(self):
        """Метод для получения урона"""
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Уничтожаем, если здоровье закончилось

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
#class Hp(pygame.sprite.Sprite):
 #   def __init__(self, x, y):
  #      super().__init__()
   #     self.image = pygame.image.load('assets/HealthsWhiteBorder.png').convert_alpha()
    #    self.rect.y = y
       # self.speed = 5
