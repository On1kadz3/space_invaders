import pygame
import sys
from bullet import Bullet

def events(screen, laser_turret, bullets):
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Право
            if event.key == pygame.K_RIGHT:
                laser_turret.move_right = True
            # Лево
            elif event.key == pygame.K_LEFT:
                laser_turret.move_left = True
            # Выстрел
            elif event.key == pygame.K_UP:
                new_bullet = Bullet(screen, laser_turret)
                bullets.add(new_bullet)


        elif event.type == pygame.KEYUP:
            # Право
            if event.key == pygame.K_RIGHT:
                laser_turret.move_right = False
            # Лево
            elif event.key == pygame.K_LEFT:
                laser_turret.move_left = False


def screen_update(bg_color, screen, laser_turret, bullets):
    # Обновление экрана
    screen.fill(bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    laser_turret.output()
    pygame.display.flip()

def update_bullets(bullets):
    # Обновление позиции пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

