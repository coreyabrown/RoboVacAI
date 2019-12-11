import pygame

width = 1024
height = 768
fps = 30
cleanColor = (255, 248, 220)
background = pygame.image.load('./wood_floor.jpg')


class Vacuum(pygame.sprite.Sprite):

    def __init__(self, displayscreen):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./robot_vacuum.png')
        self.x = int(width / 2)
        self.y = int(height / 2)

        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.screen = displayscreen

        self.size = self.image.get_rect().size
        self.center = (int(self.size[0] / 2), int(self.size[1] / 2))

        self.display(self.x, self.y)

    def display(self, x, y):
        self.screen.blit(self.image, (x, y))
        self.rect.x, self.rect.y = x, y

    def move(self):
        self.y -= 2
        self.clean(self.x, self.y)
        self.display(self.x, self.y)

    def clean(self, x, y):
        pygame.draw.circle(background, cleanColor, (x + self.center[0], y + self.center[1]), 50)
