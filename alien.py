import pygame
from random import randint


class Alien(pygame.sprite.Sprite):
    """Класс одного пришельца"""
    def __init__(self, screen):
        """Инициализация и задача начальной позиции"""
        super(Alien, self).__init__()
        self.screen = screen
        num = randint(1,2)
        self.image = pygame.image.load(f'images/alien{num}.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self):
        """Отрисовка пришельца на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self, stats):
        """Перемещение пришельцев"""
        self.y += 0.2 * 0.35 * stats.level
        self.rect.y = self.y
