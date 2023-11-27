import pygame


class Stats:
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализания статистики"""
        self.reset_stats()
        self.start_game()
        self.run_game = False
        with open('highscore.txt', 'r') as f:
            self.highscore = int(f.readline())

    def start_game(self):
        self.run_game = True
    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.lt_left = 3
        self.score = 0
