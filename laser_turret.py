import pygame


class Laser_Turret():

    def __init__(self, screen):
        # Инициализация пушки

        self.screen = screen
        self.image = pygame.image.load("images/laser-turret.png")
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

    def update_LT(self):
        # Обновление позиции
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += 1
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= 1

        self.rect.centerx = self.center

    def create_lt(self):
        """размещает пушку по центру внизу"""
        self.center = self.screen_rect.centerx
