import pygame.font


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('OCR A Becker RUS-LAT', 46)
        """Кнопка "НАЧАТЬ ИГРУ" из текста в изображение"""
        self.start_button_img = self.font.render("НАЧАТЬ ИГРУ",
                                                 True,
                                                 self.text_color,
                                                 (0, 0, 0))
        self.start_button_rect = self.start_button_img.get_rect()
        self.start_button_rect.x = self.start_button_rect.width
        self.start_button_rect.y = self.start_button_rect.height
        """Кнопка "ВЫХОД" из текста в изображение"""
        self.exit_button_img = self.font.render("ВЫЙТИ",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.exit_button_rect = self.exit_button_img.get_rect()
        self.exit_button_rect.x = self.exit_button_rect.width
        self.exit_button_rect.y = self.exit_button_rect.height
        """Позиции кнопок на экране"""
        self.start_button_pos = (self.screen_rect.width // 2 - self.start_button_rect.x // 2,
                                 self.screen_rect.height // 2 - self.start_button_rect.y // 2)
        self.exit_button_pos = (self.screen_rect.width // 2 - self.exit_button_rect.x // 2,
                                self.screen_rect.height // 2 - self.exit_button_rect.y // 2 + 100)
        """Надпись КОНЕЦ ИГРЫ"""
        self.game_over_img = self.font.render("КОНЕЦ ИГРЫ",
                                              True,
                                              self.text_color,
                                              (0, 0, 0))
        self.game_over_rect = self.game_over_img.get_rect()
        self.game_over_rect.center = self.screen_rect.center
        self.game_over_rect.centery -= 20
        """Кнопка УЛУЧШЕНИЕ ПУЛЬ"""
        self.up_bullets_img = pygame.image.load("images/bullet-upgrade.png")
        self.up_bullets_rect = self.up_bullets_img.get_rect()
        self.up_bullets_rect.center = (self.screen_rect.centerx - 150, self.screen_rect.centery)
        self.up_bullets_text = self.font.render("ПУЛИ+",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.up_bullets_text_rect = self.up_bullets_text.get_rect()
        self.up_bullets_text_rect.center = (self.up_bullets_rect.centerx, self.up_bullets_rect.centery + 150)
        """ЗАМЕДЛЕНИЕ ПРИШЕЛЬЦЕВ"""
        self.slow_aliens_img = pygame.image.load("images/slow_aliens.png")
        self.slow_aliens_rect = self.up_bullets_img.get_rect()
        self.slow_aliens_rect.center = (self.screen_rect.centerx + 150, self.screen_rect.centery)
        self.slow_aliens_text = self.font.render("ПРИШЕЛЬЦЫ--",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.slow_aliens_text_rect = self.slow_aliens_text.get_rect()
        self.slow_aliens_text_rect.center = (self.slow_aliens_rect.centerx, self.slow_aliens_rect.centery + 150)
        """Текст Выберите навык: """
        self.choose_perk = self.font.render("ВЫБЕРИТЕ НАВЫК:",
                                            True,
                                            self.text_color,
                                            (0, 0, 0))

        self.win_img = self.font.render("Поздравляю с победой!\nУвидимся в следующий раз ;)",
                                                 True,
                                                 self.text_color,
                                                 (0, 0, 0))
        self.win_rect = self.win_img.get_rect()
        self.win_rect.x = self.win_rect.width
        self.win_rect.y = self.win_rect.height

    def win(self):
        self.screen.blit(self.win_img, self.win_rect)
        self.exit_button_rect.top = self.win_rect.bottom + 10
        self.screen.blit(self.exit_button_img, self.exit_button_rect)


    def show_buttons(self):
        self.screen.blit(self.start_button_img, self.start_button_pos)
        self.screen.blit(self.exit_button_img, self.exit_button_pos)

    def show_over(self, stats):
        self.screen.blit(self.game_over_img, self.game_over_rect)
        self.accuracy_stat = self.font.render("Точность: "+str(stats.accuracy)+"%",
                                              True,
                                              self.text_color,
                                              (0, 0, 0))
        self.accuracy_stat_rect = self.accuracy_stat.get_rect()
        self.accuracy_stat_rect.top = self.game_over_rect.bottom
        self.accuracy_stat_rect.centerx = self.game_over_rect.centerx
        self.screen.blit(self.accuracy_stat, self.accuracy_stat_rect)

    def choosing_perks(self, stats):
        if stats.upgraded and not stats.slow_alien:
            self.slow_aliens_rect.center = self.screen_rect.center
            self.slow_aliens_text_rect.center = (self.slow_aliens_rect.centerx, self.slow_aliens_rect.centery + 150)
            self.screen.blit(self.slow_aliens_img, self.slow_aliens_rect)
            self.screen.blit(self.slow_aliens_text, self.slow_aliens_text_rect)
        elif not stats.upgraded and stats.slow_alien:
            self.up_bullets_rect.center = self.screen_rect.center
            self.up_bullets_text_rect.center = (self.up_bullets_rect.centerx, self.up_bullets_rect.centery + 150)
            self.screen.blit(self.up_bullets_img, self.up_bullets_rect)
            self.screen.blit(self.up_bullets_text, self.up_bullets_text_rect)
        elif not stats.upgraded and not stats.slow_alien:
            self.screen.blit(self.up_bullets_img, self.up_bullets_rect)
            self.screen.blit(self.up_bullets_text, self.up_bullets_text_rect)
            self.screen.blit(self.slow_aliens_img, self.slow_aliens_rect)
            self.screen.blit(self.slow_aliens_text, self.slow_aliens_text_rect)

