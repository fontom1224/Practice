import pygame
import random
from sprites import Ship, Bullet, Asteroid, Hp


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()
bg_original = pygame.image.load('assets/fon.png')
bg_image = pygame.transform.scale(bg_original, (800, 600))
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
                bullet = Bullet(ship.rect.centerx, ship.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

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
                score += asteroid.points
            break  # одна пуля – один астероид

    # Столкновение корабля с астероидами
    dtp = pygame.sprite.spritecollide(ship, asteroids, True)  
    if dtp:
        lives -= 1
        if lives <= 0:
            running = False
        else:
            heart_sprites.remove(all)
            all_sprites.remove(heart_sprites)
            update_hearts()  

    # Отрисовка
    all_sprites.draw(screen)

    # Отображение счёта
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    pygame.display.flip()

pygame.quit()
