import controls
import pygame
from laser_turret import Laser_Turret
from pygame.sprite import Group


def run():
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Space Invaders")
    bg_color = (0, 0, 0)
    laser_turret = Laser_Turret(screen)
    bullets = Group()


    while True:
        controls.events(screen, laser_turret, bullets)
        laser_turret.update_LT()
        controls.screen_update(bg_color, screen, laser_turret, bullets)
        controls.update_bullets(bullets)



run()
