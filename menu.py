import pygame.font


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 46)
        """Кнопка "НАЧАТЬ ИГРУ" из текста в изображение"""
        self.start_button_img = self.font.render("Начать игру!",
                                                 True,
                                                 self.text_color,
                                                 (0, 0, 0))
        self.start_button_rect = self.start_button_img.get_rect()
        self.start_button_rect.x = self.start_button_rect.width
        self.start_button_rect.y = self.start_button_rect.height
        """Кнопка "ВЫХОД" из текста в изображение"""
        self.exit_button_img = self.font.render("ВЫХОД",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.exit_button_rect = self.start_button_img.get_rect()
        self.exit_button_rect.x = self.exit_button_rect.width
        self.exit_button_rect.y = self.exit_button_rect.height
        """Позиции кнопок на экране"""
        self.start_button_pos = (self.screen_rect.width // 2 - self.start_button_rect.x // 2,
                                 self.screen_rect.height // 2 - self.start_button_rect.y // 2)
        self.exit_button_pos = (self.screen_rect.width // 2 - self.exit_button_rect.x // 2,
                                self.screen_rect.height // 2 - self.exit_button_rect.y // 2 + 100)

    def show_buttons(self):
        self.screen.blit(self.start_button_img, self.start_button_pos)
        self.screen.blit(self.exit_button_img, self.exit_button_pos)
