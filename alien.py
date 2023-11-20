import pygame

class Alien(pygame.sprite.Sprite):
    # Класс одного пришельца
    def __init__(self, screen):
        # Инициализация и задача начальной позиции
        super(Alien, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self):
        # Отрисовка пришельца на экране
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Перемещение пришельцев
        self.y += 0.1
        self.rect.y = self.y


