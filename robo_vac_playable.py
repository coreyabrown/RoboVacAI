import pygame
import sys
import vacuum_environment as env


def play():
    pygame.init()
    clean = False
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((env.width, env.height))
    pygame.display.set_caption('Robot Vacuum Playable')
    vacuum = env.Vacuum(display)

    while not clean:
        keys = pygame.key.get_pressed()
        display.blit(env.background, (0, 0))
        env.Vacuum.display(vacuum, vacuum.x, vacuum.y)

        # Game controls
        if keys[pygame.K_UP]:
            vacuum.move()
        if keys[pygame.K_RIGHT]:
            vacuum.rotate_right()
        if keys[pygame.K_LEFT]:
            vacuum.rotate_left()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print(env.calc_clean_percent())

        # Scoring and timing


        pygame.display.update()
        clock.tick(env.fps)


play()
