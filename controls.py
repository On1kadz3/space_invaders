import pygame
import sys
from bullet import Bullet
from alien import Alien

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


def screen_update(bg_color, screen, laser_turret, aliens, bullets):
    # Обновление экрана
    screen.fill(bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    laser_turret.output()
    aliens.draw(screen)
    pygame.display.flip()

def update_bullets(bullets):
    # Обновление позиции пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_aliens(aliens):
    # Обновляет позиции инопланетян
    aliens.update()

def create_army(screen, aliens):
    # Создание армии пришельцев
    alien = Alien(screen)
    alien_width = alien.rect.width
    number_alien_x = int((700 - 2 * alien_width) / alien_width)
    alien_height = alien.rect.height
    number_alien_y = int((800 - 100 - 2 * alien_height) / alien_height)

    for num_of_rows in range(number_alien_y - 2):
        for num_of_alien in range(number_alien_x):
            alien = Alien(screen)
            alien.x = alien_width + (alien_width * num_of_alien)
            alien.y = alien_height + (alien_height * num_of_rows)
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + (alien.rect.height * num_of_rows)
            aliens.add(alien)
