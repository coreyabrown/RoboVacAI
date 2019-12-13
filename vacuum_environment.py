import pygame
import math

width = 1024
height = 768
fps = 30
cleanColor = (255, 248, 220)
background = pygame.image.load('./wood_floor.jpg')
deg = 5
speed = 5


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
        self.center = self.get_center()

        self.dir = 0

        self.display(self.x, self.y)

    def get_center(self):
        center = (int(self.size[0] / 2), int(self.size[1] / 2))
        return center

    def display(self, x, y):
        # self.screen.blit(self.image, (x, y))
        # self.rect.x, self.rect.y = x, y
        center = self.get_center()
        pos = (x + (self.height / 2), y + (self.height / 2))
        self.blit_rotate(self.screen, self.image, pos, center, self.dir)

    def clean(self, x, y):
        # Need to keep track of what is "cleaned" so that I can eventually add score and fitness
        pygame.draw.circle(background, cleanColor, (x + self.center[0], y + self.center[1]), 50)

    def move(self):
        direction = self.get_vector(self.dir)
        if width - self.height > self.x - direction[0] > 0 and height - self.height > self.y - direction[1] > 0:
            self.x -= direction[0]
            self.y -= direction[1]
        self.clean(self.x, self.y)
        self.display(self.x, self.y)

    def rotate_right(self):
        pos = (self.x + (self.height / 2), self.y + (self.height / 2))
        center = self.get_center()
        self.dir -= deg
        self.blit_rotate(self.screen, self.image, pos, center, self.dir)

    def rotate_left(self):
        pos = (self.x + (self.height / 2), self.y + (self.height / 2))
        center = self.get_center()
        self.dir += deg
        self.blit_rotate(self.screen, self.image, pos, center, self.dir)

    def get_vector(self, direction):
        angle = math.radians(direction)
        vector = [int(speed * math.sin(angle)), int(speed * math.cos(angle))]
        return vector

    def blit_rotate(self, surf, image, pos, originpos, angle):

        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originpos[0], -originpos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
        pos[0] - originpos[0] + min_box[0] - pivot_move[0], pos[1] - originpos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        # rotate and blit the image
        surf.blit(rotated_image, origin)
