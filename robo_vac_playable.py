import pygame
import sys
import vacuum_environment as env


def play():
    pygame.init()
    clean = False
    cleanPercent = 0.00
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((env.width, env.height))
    pygame.display.set_caption('Robot Vacuum AI')
    vacuum = env.Vacuum(display)

    while not clean:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.blit(env.background, (0, 0))
        vacuum.move()

        pygame.display.update()
        clock.tick(env.fps)


play()
