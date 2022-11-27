import pygame


class Image:
    def __init__(self, x, y, url) -> None:
        self.x = x
        self.y = y
        self.url = url
        self.angle = 0

    def draw(self, win):
        image = pygame.image.load(self.url)
        image = pygame.transform.rotate(image, self.angle)
        win.blit(image, (self.x, self.y))

    def rotate(self, angle):
        self.angle = angle

    def setURL(self, url):
        self.url = url

    def update(self, x, y):
        self.x = x
        self.y = y
