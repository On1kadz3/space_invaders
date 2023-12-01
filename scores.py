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
        self.font = pygame.font.SysFont('OCR A Becker RUS-LAT', 14)
        self.score_to_image()
        self.highscore_to_image()
        self.level_to_image()
        self.draw_lt()

    def score_to_image(self):
        """ Текст счёта в графичесоке изображение """
        self.score_image = self.font.render(str("Текущий счёт: " + str(self.stats.score)),
                                            True, self.text_color,
                                            (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 25
        self.score_rect.top = 15

    def highscore_to_image(self):
        """Текст рекорда в граф.изображение"""
        self.hi_score_image = self.font.render(str("Лучший рекорд: " + str(self.stats.highscore)),
                                               True,
                                               self.text_color,
                                               (0, 0, 0))
        self.high_score_rect = self.hi_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 15

    def level_to_image(self):
        """Текст уровня в граф.изображение"""
        self.level_image = self.font.render(("Уровень: " + str(self.stats.level)),
                                            True,
                                            self.text_color,
                                            (0, 0, 0))
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 25
        self.level_rect.top = self.score_rect.bottom + 10

    def draw_lt(self):
        """кол-во жизней"""
        self.lts = Group()
        if self.stats.lt_left <= 4:
            for lt_number in range(self.stats.lt_left):
                lt = LaserTurret(self.screen)
                lt.image = lt.mini_image
                lt.rect.x = self.screen_rect.right - (lt_number + 1) * lt.mini_rect.width
                lt.rect.y = 15
                self.lts.add(lt)
        else:
            lt = LaserTurret(self.screen)
            lt.image = lt.mini_image
            lt.rect.x = self.screen_rect.right - lt.mini_rect.width
            lt.rect.y = 15
            self.lt_left_text = self.font.render(str(self.stats.lt_left) + "x",
                                                 True, self.text_color,
                                                 (0, 0, 0))
            self.lt_left_text_rect = self.lt_left_text.get_rect()
            self.lt_left_text_rect.right = lt.rect.left - 10
            self.lt_left_text_rect.y = 24
            self.lts.add(lt)

    def show_score(self):
        """Вывод на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hi_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.stats.lt_left <= 4:
            self.lts.draw(self.screen)
        else:
            self.lts.draw(self.screen)
            self.screen.blit(self.lt_left_text, self.lt_left_text_rect)
