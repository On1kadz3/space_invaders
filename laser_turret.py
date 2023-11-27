import pygame
from pygame.sprite import Sprite


class LaserTurret(Sprite):
    def __init__(self, screen):
        # Инициализация пушки
        super(LaserTurret, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("images/laser-turret.png")
        self.mini_image = pygame.image.load("images/mini_LT.png")
        self.mini_rect = self.mini_image.get_rect()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.move_right = False
        self.move_left = False

    def output(self):
        # Отрисовка пушки
        self.screen.blit(self.image, self.rect)

    def mini_output(self):
        """Отрисовка мини-пушки"""
        self.screen.blit(self.mini_image, self.mini_rect)

    def update_LT(self):
        # Обновление позиции
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += 2
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= 2

        self.rect.centerx = self.center

    def create_lt(self):
        """размещает пушку по центру внизу"""
        self.center = self.screen_rect.centerx
