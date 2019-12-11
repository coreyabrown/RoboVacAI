import pygame

width = 1024
height = 768
fps = 30
red = (255, 0, 0)
background = pygame.image.load('./wood_floor.jpg')


class Vacuum(pygame.sprite.Sprite):

    def __init__(self, displayscreen):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./robot_vacuum.png')
        self.x = width / 2
        self.y = height / 2

        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.screen = displayscreen

        self.display(self.x, self.y)

    def display(self, x, y):
        self.screen.blit(self.image, (x, y))
        self.rect.x, self.rect.y = x, y

    def move(self):
        self.display(self.x, self.y)
