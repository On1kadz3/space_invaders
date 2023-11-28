import pygame


class Stats:
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализания статистики"""
        self.level = None
        self.reset_stats()
        self.start_game()
        self.game_over = False
        self.run_game = False
        with open('highscore.txt', 'r') as f:
            self.highscore = int(f.readline())

    def start_game(self):
        self.level = 0
        self.run_game = True

    def over_game(self):
        self.game_over = True


    def levelup(self,scores):
        self.level += 1
        scores.level_to_image()


    def leveldown(self,scores):
        self.level -= 1
        scores.level_to_image()

    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.lt_left = 3
        self.score = 0
