import pygame


class Stats:
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализания статистики"""
        self.accuracy = None
        self.level = None
        self.reset_stats()
        self.start_game()
        self.win_game = False
        self.upgraded = False
        self.game_over = False
        self.slow_alien = False
        self.run_game = False
        self.choose_perk = False
        self.level_reached = False
        with open('highscore.txt', 'r') as f:
            self.highscore = int(f.readline())

    def start_game(self):
        self.level = 29
        self.run_game = True

    def accuracy_count(self, bullet_counter, accuracy_counter):
        try: self.accuracy = accuracy_counter / bullet_counter
        except ZeroDivisionError as e:
            self.accuracy = 1
        self.accuracy = int((1 - round(self.accuracy, 2)) * 100)

    def over_game(self):
        self.game_over = True

    def levelup(self, scores):
        self.level += 1
        scores.level_to_image()

    def leveldown(self, scores):
        self.level -= 1
        scores.level_to_image()

    def bullet_up(self):
        self.upgraded = True

    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.lt_left = 0
        self.score = 0
