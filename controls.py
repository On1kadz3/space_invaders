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


def screen_update(bg_color, screen, stats, scores, laser_turret, aliens, bullets):
    """ Обновление экрана """
    screen.fill(bg_color)
    scores.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    laser_turret.output()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(screen, stats, scores, aliens, bullets):
    """ Обновление позиции пуль """
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += 50 * len(aliens)
        scores.score_to_image()
        check_hi_score(stats, scores)
        scores.draw_LT()
    if len(aliens) == 0:
        bullets.empty()
        create_army(screen, aliens)


def lt_kill(stats, screen, scores, laser_turret, aliens, bullets):
    """Столкновение пушки и пришельцев"""
    if stats.lt_left > 0:
        stats.lt_left -= 1
        scores.draw_LT()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens)
        laser_turret.create_lt()
        time.sleep(1.5)
    else:
        stats.run_game = False
        sys.exit()


def update_aliens(stats, screen, scores, laser_turret, aliens, bullets):
    # Обновляет позиции инопланетян
    aliens.update()
    if pygame.sprite.spritecollideany(laser_turret, aliens):
        lt_kill(stats, screen, scores, laser_turret, aliens, bullets)
    aliens_check(stats, screen, scores, laser_turret, aliens, bullets)


def aliens_check(stats, screen, scores, laser_turret, aliens, bullets):
    """Проверка на соприкосновение пришельцев с краем экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            lt_kill(stats, screen, scores, laser_turret, aliens, bullets)
            break


def create_army(screen, aliens):
    """Создание армии пришельцев"""
    alien = Alien(screen)
    alien_width = alien.rect.width
    number_alien_x = int((700 - 2 * alien_width) / alien_width)
    alien_height = alien.rect.height
    number_alien_y = int((800 - 100 - 2 * alien_height) / alien_height)

    for num_of_rows in range(number_alien_y - 2):
        for num_of_alien in range(number_alien_x):
            alien = Alien(screen)
            alien.x = alien_width + (alien_width * num_of_alien)
            alien.y = alien_height + (alien_height * num_of_rows) + 20
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + (alien.rect.height * num_of_rows)
            aliens.add(alien)


def check_hi_score(stats, scores):
    """ Проверка новых рекордов"""
    if stats.score > stats.highscore:
        stats.highscore = stats.score
        scores.highscore_to_image()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.highscore))
