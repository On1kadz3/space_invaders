import pygame

def run_music(music_name):
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.get_volume()
