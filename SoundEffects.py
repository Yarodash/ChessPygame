import pygame


class SoundEffects:

    def __init__(self):
        self.move_sound = pygame.mixer.Sound('Sounds/move_sound.mp3')
        self.capture_sound = pygame.mixer.Sound('Sounds/capture_sound.mp3')
        self.stalemate_sound = pygame.mixer.Sound('Sounds/stalemate_sound.mp3')
        self.check_sound = pygame.mixer.Sound('Sounds/check_sound.mp3')
        self.victory_sound = pygame.mixer.Sound('Sounds/victory_sound.mp3')


__all__ = ['SoundEffects']
