import pygame
import sys
import vacuum_environment as env


def play():
    pygame.init()
    start_time = pygame.time.get_ticks()
    clean = False
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((env.width, env.height))
    pygame.display.set_caption('Robot Vacuum Playable')
    vacuum = env.Vacuum(display)
    font = pygame.font.Font(None, 54)
    font_color = pygame.Color('white')
    black = (0, 0, 0)

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
        passed_time = pygame.time.get_ticks() - start_time
        pygame.draw.rect(env.background, black, (10, 10, 260, 150))
        time = font.render('Time: ' + str(round(passed_time / 1000, 2)), True, font_color)
        env.background.blit(time, (20, 20))
        cleaned = font.render('Clean: ' + str(env.calc_clean_percent()), True, font_color)
        env.background.blit(cleaned, (20, 70))
        score = round((env.calc_clean_percent() * 100) ** 2 / ((passed_time / 1000) + .01), 2)
        score_display = font. render('Score: ' + str(score), True, font_color)
        env.background.blit(score_display, (20, 120))

        if env.calc_clean_percent() >= .9 or passed_time / 1000 >= 300:
            print('Game Over. You scored ' + str(score) + ' points')
            print('Clean percentage: ' + str(env.calc_clean_percent() * 100))
            clean = True

        pygame.display.update()
        clock.tick(env.fps)


play()
