import pygame
pygame.mixer.init()

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/ship.png').convert_alpha()
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
        self.image = pygame.image.load('images/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load('images/asteroid.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -40
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


"""
#Спрайт бонуса
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, effect_type, speed=2):
        super().__init__()
        self.image = pygame.image.load('images/powerup.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x          # позиция X
        self.rect.y = y          # позиция Y
        self.speed = speed       # дополнительная характеристика
        self.effect = effect_type # тип бонуса (например, 'speed', 'shield')
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
powerup = PowerUp(300, 50, 'shield', 3)

#спрайт астероида
asteroid = Asteroid(x=150)  # позиция по X = 150, Y устанавливается в -40 внутри класса

#Загрузка муз. файла
pygame.mixer.music.load('sounds/background_music.ogg')

#Начать воспроизведение файла
pygame.mixer.music.play(-1)

#Изменение громкости
pygame.mixer.music.set_volume(0.5)

#Пауза
# pygame.mixer.music.pause()

#Возобновление
pygame.mixer.music.unpause()

#Остановка
#pygame.mixer.music.stop()

#Звуковые эффекты
laser_sound = pygame.mixer.Sound('sounds/laser.wav')
laser_sound.play()
laser_sound.set_volume(0.3)
"""
