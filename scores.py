import pygame.font
from laser_turret import LaserTurret
from pygame.sprite import Group


class Scores:
    """ Вывод игровой информации"""

    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 24)
        self.score_to_image()
        self.highscore_to_image()
        self.draw_LT()

    def score_to_image(self):
        """ Текст счёта в графичесоке изображение """
        self.score_image = self.font.render(str("Текущий счёт: "+str(self.stats.score)), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 25
        self.score_rect.top = 15

    def highscore_to_image(self):
        """Текст рекорда в граф.изображение"""
        self.hi_score_image = self.font.render(str("Лучший рекорд: "+str(self.stats.highscore)),
                                               True,
                                               self.text_color,
                                               (0, 0, 0))
        self.high_score_rect = self.hi_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 15

    def draw_LT(self):
        """кол-во жизней"""
        self.lts = Group()
        for lt_number in range(self.stats.lt_left):
            lt = LaserTurret(self.screen)
            lt.image = lt.mini_image
            lt.rect.x = self.screen_rect.right - (lt_number + 1) * lt.mini_rect.width
            lt.rect.y = 15
            self.lts.add(lt)

    def show_score(self):
        """Вывод на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hi_score_image, self.high_score_rect)
        self.lts.draw(self.screen)
