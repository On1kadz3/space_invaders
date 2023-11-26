import controls
import pygame
from laser_turret import LaserTurret
from pygame.sprite import Group
from stats import Stats
from scores import Scores


def run():
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Space Invaders")
    bg_color = (0, 0, 0)
    laser_turret = LaserTurret(screen)
    bullets = Group()
    aliens = Group()
    controls.create_army(screen, aliens)
    stats = Stats()
    scores = Scores(screen, stats)

    while True:
        controls.events(screen, laser_turret, bullets)
        if stats.run_game:
            laser_turret.update_LT()
            controls.screen_update(bg_color, screen, stats, scores, laser_turret, aliens, bullets)
            controls.update_bullets(screen, stats, scores, aliens, bullets)
            controls.update_aliens(stats, screen, scores, laser_turret, aliens, bullets)


run()
