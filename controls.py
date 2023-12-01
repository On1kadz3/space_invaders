import pygame
import sys

from bullet import Bullet
from alien import Alien
import time

mute_sound, mute_music, paused = False, False, False
bullet_lvl, counter = 1, 0  # accuracy_counter, bullet_counter = 1, 0, 0, 0


def events(screen, laser_turret, bullets, stats, menu):
    # Обработка событий
    global mute_sound, paused, mute_music, bullet_lvl  # , bullet_counter
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
            elif event.key == pygame.K_m:
                mute_sound = not mute_sound
            # Выстрел
            elif event.key == pygame.K_SPACE and not paused and stats.run_game and not stats.choose_perk:
                bullet_lvl = 1  # + (stats.score // 25000)
                for new_bullet in range(bullet_lvl):
                    new_bullet = Bullet(screen, laser_turret, stats)
                    # bullet_counter += 1
                    bullets.add(new_bullet)
                if not mute_sound:
                    pygame.mixer.Sound("sounds/laser-piu.wav").play()
            # Пауза музыки
            elif event.key == pygame.K_RSHIFT:
                mute_music = not mute_music
                if mute_music:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif (event.key == pygame.K_p or event.key == pygame.K_ESCAPE) and stats.run_game:
                pygame.mixer.Sound("sounds/pause.wav").play().set_volume(0.5)
                paused = not paused
        elif event.type == pygame.KEYUP:
            # Вправо
            if event.key == pygame.K_RIGHT:
                laser_turret.move_right = False
            # Влево
            elif event.key == pygame.K_LEFT:
                laser_turret.move_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not stats.run_game:
                start_button_pos = menu.start_button_pos
                exit_button_pos = menu.exit_button_pos
                start_button = menu.start_button_rect
                exit_button = menu.exit_button_rect
                if start_button_pos[0] <= mouse_pos[0] <= start_button_pos[0] + start_button.width and \
                        start_button_pos[1] <= mouse_pos[1] <= start_button_pos[1] + start_button.height:
                    stats.start_game()
                elif exit_button_pos[0] <= mouse_pos[0] <= exit_button_pos[0] + exit_button.width and \
                        exit_button_pos[1] <= mouse_pos[1] <= exit_button_pos[1] + exit_button.height:
                    sys.exit()
            elif stats.run_game and stats.choose_perk:
                bullet_upgrade_btn = menu.up_bullets_rect
                slow_aliens_btn = menu.slow_aliens_rect
                if bullet_upgrade_btn[0] <= mouse_pos[0] <= bullet_upgrade_btn[0] + bullet_upgrade_btn.width and \
                        bullet_upgrade_btn[1] <= mouse_pos[1] <= bullet_upgrade_btn[1] + bullet_upgrade_btn.height:
                    stats.upgraded = True
                    stats.choose_perk = False
                if slow_aliens_btn[0] <= mouse_pos[0] <= slow_aliens_btn[0] + slow_aliens_btn.width and \
                        slow_aliens_btn[1] <= mouse_pos[1] <= slow_aliens_btn[1] + slow_aliens_btn.height:
                    stats.slow_alien = True
                    stats.choose_perk = False


def start_screen(bg_color, screen, menu):  # Начальный экран
    screen.fill(bg_color)
    menu.show_buttons()
    pygame.display.flip()


def game_over_screen(bg_color, screen, menu):  # Игра окончена
    pygame.mixer.music.stop()
    pygame.mixer.Sound("sounds/game_over.wav").play().set_volume(0.5)
    screen.fill(bg_color)
    menu.show_over()
    pygame.display.flip()


def choosing_perks_screen(bg_color, screen, menu, stats):  # Экран выбора перков
    screen.fill(bg_color)
    menu.choosing_perks(stats)
    pygame.display.flip()


def screen_update(bg_color, screen, scores, laser_turret, aliens, bullets, fps):
    """ Обновление экрана """
    screen.fill(bg_color)
    scores.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    laser_turret.output()
    aliens.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(fps)


def update_bullets(screen, stats, scores, aliens, bullets):
    """ Обновление позиции пуль """
    global counter  # , accuracy_counter
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # accuracy_counter += 1
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += int(50 * len(aliens) * stats.level * 0.5)
            if counter - stats.score // 100000 < 0:
                counter += 1
                stats.lt_left += 1
                pygame.mixer.Sound("sounds/1up.wav").play().set_volume(0.5)
        scores.score_to_image()
        check_hi_score(stats, scores)
        scores.draw_lt()
    if len(aliens) == 0:
        bullets.empty()
        stats.levelup(scores)
        if (stats.level % 5) == 0 and not stats.level == 0 and not stats.level_reached and \
                not (stats.upgraded and stats.slow_alien):
            stats.level_reached = True
            stats.choose_perk = True
        else:
            stats.level_reached = False
            stats.choose_perk = False
        create_army(screen, aliens, stats)


def lt_kill(stats, screen, scores, laser_turret, aliens, bullets, menu):
    """Столкновение пушки и пришельцев"""
    if stats.lt_left > 0:
        stats.lt_left -= 1
        scores.draw_lt()
        create_army(screen, aliens, stats)
        laser_turret.create_lt()
        time.sleep(1.5)
        aliens.empty()
        bullets.empty()
    else:
        stats.run_game = False
        stats.over_game()


def restart_game(scores, stats, aliens, bullets, laser_turret):
    scores.draw_lt()
    aliens.empty()
    bullets.empty()
    laser_turret.create_lt()
    stats.reset_stats()


def update_aliens(stats, screen, scores, laser_turret, aliens, bullets, menu):
    """Обновляет позиции инопланетян"""
    aliens.update(stats)
    if pygame.sprite.spritecollideany(laser_turret, aliens):
        lt_kill(stats, screen, scores, laser_turret, aliens, bullets, menu)
        stats.leveldown(scores)
    aliens_check(stats, screen, scores, laser_turret, aliens, bullets, menu)


def aliens_check(stats, screen, scores, laser_turret, aliens, bullets, menu):
    """Проверка на соприкосновение пришельцев с краем экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            lt_kill(stats, screen, scores, laser_turret, aliens, bullets, menu)
            break


def create_army(screen, aliens, stats):
    """Создание армии пришельцев"""
    alien = Alien(screen)
    alien_width = alien.rect.width
    number_alien_x = int((700 - 2 * alien_width) / alien_width)
    alien_height = alien.rect.height
    number_alien_y = int((800 - 100 - 2 * alien_height) / alien_height)
    center_modifier = 4
    if (6 - stats.level // 4) >= 4:
        rows_modifier = 6 - stats.level // 4
    else:
        rows_modifier = 4
    if (center_modifier - stats.level // 2) >= 2:
        if (stats.level // 2) % 2 == 0:
            columns_modifier = center_modifier - (stats.level // 2)
        else:
            columns_modifier = center_modifier - 1 - (stats.level // 2)
    else:
        columns_modifier = 0
    for num_of_rows in range(number_alien_y - rows_modifier):
        for num_of_alien in range(number_alien_x - columns_modifier):
            alien = Alien(screen)
            alien.x = (columns_modifier // 2 + 1) * alien_width + (alien_width * num_of_alien)
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
