import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, laser_turret):
        # Создание Пули в позиции пушки
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 10)
        self.color = 0, 183, 239
        self.speed = 1
        self.rect.centerx = laser_turret.rect.centerx
        self.rect.top = laser_turret.rect.top
        self.y = float(self.rect.y)

    def update(self):
        # Перемещение пули
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        # Отрисовка пули
        pygame.draw.rect(self.screen, self.color, self.rect)