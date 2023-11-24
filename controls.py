import pygame
import sys
from bullet import Bullet
from alien import Alien
import time

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

def update_bullets(screen, aliens, bullets):
    # Обновление позиции пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_army(screen, aliens)


def lt_kill(stats, screen, laser_turret, aliens, bullets):
    """Столкновение пушки и пришельцев"""
    stats.lt_left -= 1
    aliens.empty()
    bullets.empty()
    create_army(screen, aliens)
    laser_turret.create_lt()
    time.sleep(2)


def update_aliens(stats, screen, laser_turret, aliens, bullets):
    # Обновляет позиции инопланетян
    aliens.update()
    if pygame.sprite.spritecollideany(laser_turret, aliens):
        lt_kill(stats, screen, laser_turret, aliens, bullets)
    aliens_check(stats, screen, laser_turret, aliens, bullets)

def aliens_check(stats, screen, laser_turret, aliens, bullets):
    """Проверка на соприкосновение пришельцев с краем экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            lt_kill(stats, screen, laser_turret, aliens, bullets)
            break


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