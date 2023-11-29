import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, laser_turret, stats):
        # Создание Пули в позиции пушки
        super(Bullet, self).__init__()
        self.screen = screen
        self.base_num = 5
        if stats.upgraded:
            self.rect = pygame.Rect(0, 0, self.base_num * ((stats.level // 3) + 1), 5)
        else:
            self.rect = pygame.Rect(0, 0, 600, 5)
        self.color = 0, 183, 239
        self.speed = 9.5
        self.rect.centerx = laser_turret.rect.centerx
        self.rect.top = laser_turret.rect.top
        self.y = float(self.rect.y)

    def update(self):
        # Перемещение пули
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовка пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)