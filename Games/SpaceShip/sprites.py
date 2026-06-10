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
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

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
        if asteroid_type == 1:  # Маленький метеор
            self.image_path = 'assets/asteroid1.png'
            self.size_factor = 1.0
            self.health = 1
            self.speed = 4
            self.points = 10  
        else:  # Большой метеор
            self.image_path = 'assets/asteroid2.png'
            self.size_factor = 1.1
            self.health = 3
            self.speed = 2
            self.points = 30  

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
        self.health -= 1
        if self.health <= 0:
            self.kill() 
            return True 
        return False 

class Hp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/HealthsWhiteBorder.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        # Метод нужен, чтобы не было ошибки при вызове из группы
        pass
