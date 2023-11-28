import time

import controls
import pygame
import pygame.font

from menu import Menu
from laser_turret import LaserTurret
from pygame.sprite import Group
from stats import Stats
from scores import Scores
import music

WIDTH = 700
HEIGHT = 800
FPS = 60
running = True


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    track = "sounds/megalovania.mp3"
    music.run_music(track)
    bg_color = (0, 0, 0)
    laser_turret = LaserTurret(screen)
    bullets = Group()
    aliens = Group()
    controls.create_army(screen, aliens)
    stats = Stats()
    scores = Scores(screen, stats)
    menu = Menu(screen)
    while True:
        controls.events(screen, laser_turret, bullets, stats, menu)
        if stats.run_game:
            laser_turret.update_LT(stats)
            controls.screen_update(bg_color, screen, stats, scores, menu, laser_turret, aliens, bullets, FPS)
            controls.update_bullets(screen, stats, scores, aliens, bullets)
            controls.update_aliens(stats, screen, scores, laser_turret, aliens, bullets, menu)
        elif (stats.run_game == False) and stats.game_over == True:
            controls.game_over_screen(bg_color, screen, menu)
            time.sleep(1.5)
            controls.restart_game(scores, stats, aliens, bullets, laser_turret)
            stats.game_over = False
        elif not stats.run_game and not stats.game_over:
            controls.start_screen(bg_color, screen, menu)
            controls.restart_game(scores, stats, aliens, bullets, laser_turret)


run()
