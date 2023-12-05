import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
from random import randint
import sys
import time
import asyncio


class Alien(pygame.sprite.Sprite):
    """Класс одного пришельца"""

    def __init__(self, screen):
        """Инициализация и задача начальной позиции"""
        super(Alien, self).__init__()
        self.screen = screen
        num = randint(1, 3)
        self.image = pygame.image.load(f'images/alien{num}.png')
        self.modifier = 1
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self):
        """Отрисовка пришельца на экране"""
        self.screen.blit(self.image, self.rect)

    def change_modifier(self):
        self.modifier = 3

    def update(self, stats):
        """Перемещение пришельцев"""
        if stats.slow_alien:
            self.change_modifier()
        self.y += (0.15 * 0.35 * stats.level) / self.modifier
        self.rect.y = self.y


class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, laser_turret, stats):
        """ Создание Пули в позиции пушки """
        super(Bullet, self).__init__()
        self.screen = screen
        self.base_num = 5
        if stats.upgraded:
            self.rect = pygame.Rect(0, 0, self.base_num * ((stats.level // 3) + 1), 5)
        else:
            self.rect = pygame.Rect(0, 0, 5, 5)
        self.color = 0, 183, 239
        self.speed = 9.5
        self.rect.centerx = laser_turret.rect.centerx
        self.rect.top = laser_turret.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """ Перемещение пули """
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовка пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class LaserTurret(Sprite):
    def __init__(self, screen):
        """ Инициализация пушки """
        super(LaserTurret, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("images/laser-turret.png")
        self.mini_image = pygame.image.load("images/mini_LT.png")
        self.mini_rect = self.mini_image.get_rect()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.move_right = False
        self.move_left = False

    def output(self):
        """ Отрисовка пушки """
        self.screen.blit(self.image, self.rect)

    def update_lt(self, stats):
        """ Обновление позиции """
        if stats.level <= 4:
            if self.move_right and self.rect.right < self.screen_rect.right:
                self.center += 3
            if self.move_left and self.rect.left > self.screen_rect.left:
                self.center -= 3
        else:
            if self.move_right and self.rect.right < self.screen_rect.right:
                self.center += 3 * (stats.level / 4)
            if self.move_left and self.rect.left > self.screen_rect.left:
                self.center -= 3 * (stats.level / 4)

        self.rect.centerx = self.center

    def create_lt(self):
        """размещает пушку по центру внизу"""
        self.center = self.screen_rect.centerx


class Changeable:

    def __init__(self):
        self.mute_sound = False
        self.mute_music = False
        self.paused = False
        self.counter = 0
        self.accuracy_counter = 0
        self.bullet_counter = 0


# def run_music(music_name):
#     pygame.mixer.music.load(music_name)
#     pygame.mixer.music.play(-1)
#     pygame.mixer.music.set_volume(0.3)
#     pygame.mixer.music.get_volume()


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("my_font.otf", 46)
        """Кнопка "НАЧАТЬ ИГРУ" из текста в изображение"""
        self.start_button_img = self.font.render("НАЧАТЬ ИГРУ",
                                                 True,
                                                 self.text_color,
                                                 (0, 0, 0))
        self.start_button_rect = self.start_button_img.get_rect()
        self.start_button_rect.x = self.start_button_rect.width
        self.start_button_rect.y = self.start_button_rect.height
        """Кнопка "ВЫХОД" из текста в изображение"""
        self.exit_button_img = self.font.render("ВЫЙТИ",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.exit_button_rect = self.exit_button_img.get_rect()
        self.exit_button_rect.x = self.exit_button_rect.width
        self.exit_button_rect.y = self.exit_button_rect.height
        """Позиции кнопок на экране"""
        self.start_button_pos = (self.screen_rect.width // 2 - self.start_button_rect.x // 2,
                                 self.screen_rect.height // 2 - self.start_button_rect.y // 2)
        self.exit_button_pos = (self.screen_rect.width // 2 - self.exit_button_rect.x // 2,
                                self.screen_rect.height // 2 - self.exit_button_rect.y // 2 + 100)
        """Надпись КОНЕЦ ИГРЫ"""
        self.game_over_img = self.font.render("КОНЕЦ ИГРЫ",
                                              True,
                                              self.text_color,
                                              (0, 0, 0))
        self.game_over_rect = self.game_over_img.get_rect()
        self.game_over_rect.center = self.screen_rect.center
        self.game_over_rect.centery -= 20
        """Кнопка УЛУЧШЕНИЕ ПУЛЬ"""
        self.up_bullets_img = pygame.image.load("images/bullet-upgrade.png")
        self.up_bullets_rect = self.up_bullets_img.get_rect()
        self.up_bullets_rect.center = (self.screen_rect.centerx - 150, self.screen_rect.centery)
        self.up_bullets_text = self.font.render("ПУЛИ+",
                                                True,
                                                self.text_color,
                                                (0, 0, 0))
        self.up_bullets_text_rect = self.up_bullets_text.get_rect()
        self.up_bullets_text_rect.center = (self.up_bullets_rect.centerx, self.up_bullets_rect.centery + 150)
        """ЗАМЕДЛЕНИЕ ПРИШЕЛЬЦЕВ"""
        self.slow_aliens_img = pygame.image.load("images/slow_aliens.png")
        self.slow_aliens_rect = self.up_bullets_img.get_rect()
        self.slow_aliens_rect.center = (self.screen_rect.centerx + 150, self.screen_rect.centery)
        self.slow_aliens_text = self.font.render("ПРИШЕЛЬЦЫ--",
                                                 True,
                                                 self.text_color,
                                                 (0, 0, 0))
        self.slow_aliens_text_rect = self.slow_aliens_text.get_rect()
        self.slow_aliens_text_rect.center = (self.slow_aliens_rect.centerx, self.slow_aliens_rect.centery + 150)
        """Текст Выберите навык: """
        self.choose_perk = self.font.render("ВЫБЕРИТЕ НАВЫК:",
                                            True,
                                            self.text_color,
                                            (0, 0, 0))

    def show_buttons(self):
        self.screen.blit(self.start_button_img, self.start_button_pos)
        self.screen.blit(self.exit_button_img, self.exit_button_pos)

    def show_over(self, stats):
        self.screen.blit(self.game_over_img, self.game_over_rect)
        self.accuracy_stat = self.font.render("Точность: " + str(stats.accuracy) + "%",
                                              True,
                                              self.text_color,
                                              (0, 0, 0))
        self.accuracy_stat_rect = self.accuracy_stat.get_rect()
        self.accuracy_stat_rect.top = self.game_over_rect.bottom
        self.accuracy_stat_rect.centerx = self.game_over_rect.centerx
        self.screen.blit(self.accuracy_stat, self.accuracy_stat_rect)

    def choosing_perks(self, stats):
        if stats.upgraded and not stats.slow_alien:
            self.slow_aliens_rect.center = self.screen_rect.center
            self.slow_aliens_text_rect.center = (self.slow_aliens_rect.centerx, self.slow_aliens_rect.centery + 150)
            self.screen.blit(self.slow_aliens_img, self.slow_aliens_rect)
            self.screen.blit(self.slow_aliens_text, self.slow_aliens_text_rect)
        elif not stats.upgraded and stats.slow_alien:
            self.up_bullets_rect.center = self.screen_rect.center
            self.up_bullets_text_rect.center = (self.up_bullets_rect.centerx, self.up_bullets_rect.centery + 150)
            self.screen.blit(self.up_bullets_img, self.up_bullets_rect)
            self.screen.blit(self.up_bullets_text, self.up_bullets_text_rect)
        elif not stats.upgraded and not stats.slow_alien:
            self.screen.blit(self.up_bullets_img, self.up_bullets_rect)
            self.screen.blit(self.up_bullets_text, self.up_bullets_text_rect)
            self.screen.blit(self.slow_aliens_img, self.slow_aliens_rect)
            self.screen.blit(self.slow_aliens_text, self.slow_aliens_text_rect)


class Scores:
    """ Вывод игровой информации"""

    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("my_font.otf", 26) # 'OCR A Becker RUS-LAT'
        self.score_to_image()
        self.highscore_to_image()
        self.level_to_image()
        self.draw_lt()

    def score_to_image(self):
        """ Текст счёта в графичесоке изображение """
        self.score_image = self.font.render(str("Текущий счёт: " + str(self.stats.score)),
                                            True, self.text_color,
                                            (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 25
        self.score_rect.top = 15

    def highscore_to_image(self):
        """Текст рекорда в граф.изображение"""
        self.hi_score_image = self.font.render(str("Лучший рекорд: " + str(self.stats.highscore)),
                                               True,
                                               self.text_color,
                                               (0, 0, 0))
        self.high_score_rect = self.hi_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 15

    def level_to_image(self):
        """Текст уровня в граф.изображение"""
        self.level_image = self.font.render(("Уровень: " + str(self.stats.level)),
                                            True,
                                            self.text_color,
                                            (0, 0, 0))
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 25
        self.level_rect.top = self.score_rect.bottom + 10

    def draw_lt(self):
        """кол-во жизней"""
        self.lts = Group()
        if self.stats.lt_left <= 4:
            for lt_number in range(self.stats.lt_left):
                lt = LaserTurret(self.screen)
                lt.image = lt.mini_image
                lt.rect.x = self.screen_rect.right - (lt_number + 1) * lt.mini_rect.width
                lt.rect.y = 15
                self.lts.add(lt)
        else:
            lt = LaserTurret(self.screen)
            lt.image = lt.mini_image
            lt.rect.x = self.screen_rect.right - lt.mini_rect.width
            lt.rect.y = 15
            self.lt_left_text = self.font.render(str(self.stats.lt_left) + "x",
                                                 True, self.text_color,
                                                 (0, 0, 0))
            self.lt_left_text_rect = self.lt_left_text.get_rect()
            self.lt_left_text_rect.right = lt.rect.left - 10
            self.lt_left_text_rect.y = 24
            self.lts.add(lt)

    def show_score(self):
        """Вывод на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hi_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.stats.lt_left <= 4:
            self.lts.draw(self.screen)
        else:
            self.lts.draw(self.screen)
            self.screen.blit(self.lt_left_text, self.lt_left_text_rect)


class Stats:
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализания статистики"""
        self.accuracy = None
        self.level = None
        self.reset_stats()
        self.start_game()
        self.upgraded = False
        self.game_over = False
        self.slow_alien = False
        self.run_game = False
        self.choose_perk = False
        self.level_reached = False
        with open('highscore.txt', 'r') as f:
            self.highscore = int(f.readline())

    def start_game(self):
        self.level = 0
        self.run_game = True

    def accuracy_count(self, ch):
        self.accuracy = ch.accuracy_counter / ch.bullet_counter
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
        self.lt_left = 3
        self.score = 0


async def events(screen, laser_turret, bullets, stats, menu, ch):
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
            elif event.key == pygame.K_m:
                ch.mute_sound = not ch.mute_sound
            # Выстрел
            elif event.key == pygame.K_SPACE and not ch.paused and stats.run_game and not stats.choose_perk:
                new_bullet = Bullet(screen, laser_turret, stats)
                ch.bullet_counter += 1
                bullets.add(new_bullet)
                # if not ch.mute_sound:
                #     pygame.mixer.Sound("sounds/laser-piu.wav").play()
            # Пауза музыки
            # elif event.key == pygame.K_RSHIFT:
            #     ch.mute_music = not ch.mute_music
            #     if ch.mute_music:
            #         pygame.mixer.music.pause()
            #     else:
            #         pygame.mixer.music.unpause()
            elif (event.key == pygame.K_p or event.key == pygame.K_ESCAPE) and stats.run_game:
                # pygame.mixer.Sound("sounds/pause.wav").play().set_volume(0.5)
                ch.paused = not ch.paused
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
        await asyncio.sleep(0)


def start_screen(bg_color, screen, menu):  # Начальный экран
    screen.fill(bg_color)
    menu.show_buttons()
    pygame.display.flip()


def game_over_screen(bg_color, screen, menu, stats, ch):  # Игра окончена
    # pygame.mixer.music.stop()
    # pygame.mixer.Sound("sounds/game_over.wav").play().set_volume(0.5)
    stats.accuracy_count(ch.bullet_counter, ch.accuracy_counter)
    screen.fill(bg_color)
    menu.show_over(stats)
    pygame.display.flip()
    time.sleep(6.5)
    # pygame.mixer.music.load("sounds/megalovania.mp3")
    # pygame.mixer.music.play(-1)
    paused = False


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


def update_bullets(screen, stats, scores, aliens, bullets, ch):
    """ Обновление позиции пуль """
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            ch.accuracy_counter += 1
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += int(50 * len(aliens) * stats.level * 0.5)
            if ch.counter - stats.score // 100000 < 0:
                ch.counter += 1
                stats.lt_left += 1
                # pygame.mixer.Sound("sounds/1up.wav").play().set_volume(0.5)
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
    number_alien_x = int((screen.get_width() - 2 * alien_width) / alien_width)
    alien_height = alien.rect.height
    number_alien_y = int((screen.get_height() - 100 - 2 * alien_height) / alien_height)
    center_modifier = 4
    if (6 - stats.level // 4) >= 3:
        rows_modifier = 6 - stats.level // 4
    else:
        rows_modifier = 3
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


WIDTH = 700
HEIGHT = 750
FPS = 60


async def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    # track = "sounds/megalovania.mp3"
    # run_music(track)
    bg_color = (0, 0, 0)
    laser_turret = LaserTurret(screen)
    bullets = Group()
    aliens = Group()
    stats = Stats()
    create_army(screen, aliens, stats)
    scores = Scores(screen, stats)
    menu = Menu(screen)
    ch = Changeable()
    while True:
        await events(screen, laser_turret, bullets, stats, menu, ch)
        if not ch.paused:
            if stats.run_game:
                if stats.level_reached and stats.choose_perk and (not stats.slow_alien or not stats.upgraded):
                    choosing_perks_screen(bg_color, screen, menu, stats)
                else:
                    laser_turret.update_lt(stats)
                    screen_update(bg_color, screen, scores, laser_turret, aliens, bullets, FPS)
                    update_bullets(screen, stats, scores, aliens, bullets, ch)
                    update_aliens(stats, screen, scores, laser_turret, aliens, bullets, menu)
            elif not stats.run_game and stats.game_over:
                game_over_screen(bg_color, screen, menu, stats, ch)
                restart_game(scores, stats, aliens, bullets, laser_turret)
                stats.game_over = False
            elif not stats.run_game and not stats.game_over:
                start_screen(bg_color, screen, menu)
                restart_game(scores, stats, aliens, bullets, laser_turret)
        await asyncio.sleep(0)


asyncio.run(run())
