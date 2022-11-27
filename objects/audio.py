import pygame


class Audio:
    def __init__(self, url) -> None:
        self.url = url

    def play(self):
        pygame.mixer.music.load(self.url)
        pygame.mixer.music.play(0)
