import pygame

class Stats():
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализания статистики"""
        self.reset_stats()
    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.lt_left = 3
