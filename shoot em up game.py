import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

bullet_img = pygame.Surface((10, 20))
bullet_img.fill((0, 255, 0))
player_img = pygame.transform.scale(pygame.image.load("playerr.png"), (60, 60))
enemy_img = pygame.transform.scale(pygame.image.load("enemy.png"), (70, 70))

class Player:
    def __init__(self):
        self.image = player_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 12
        self.bullets = []

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.image.get_width():
            self.x = WIDTH - self.image.get_width()

    def shoot(self):
        bullet = Bullet(self.x + self.image.get_width() // 2, self.y)
        self.bullets.append(bullet)

class Enemy:
    def __init__(self, speed):
        self.image = enemy_img
        self.x = random.randint(0, WIDTH - self.image.get_width())
        self.y = random.randint(-100, -40)
        self.speed = speed

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img
        self.x = x
        self.y = y
        self.speed = 10

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= self.speed

def main():
    run = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy(1) for i in range(5)]
    missed_enemies = 0
    killed_enemies = 0
    enemy_speed = 1

    while run:
        clock.tick(30)
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)
        if keys[pygame.K_SPACE]:
            player.shoot()

        for bullet in player.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.move()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                enemies.append(Enemy(enemy_speed))
                missed_enemies += 1
                if missed_enemies >= 5:
                    run = False
            for bullet in player.bullets[:]:
                if (enemy.x < bullet.x < enemy.x + enemy.image.get_width() and
                        enemy.y < bullet.y < enemy.y + enemy.image.get_height()):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    enemies.append(Enemy(enemy_speed))
                    killed_enemies += 1
                    break

        if killed_enemies % 20 == 0 and killed_enemies > 0:
            enemy_speed += 0.02

        player.draw()
        for bullet in player.bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {killed_enemies}', True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()

    win.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    score_text = font.render(f'Score: {killed_enemies}', True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + text.get_height()))
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()


