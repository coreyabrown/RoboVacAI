import pygame
import sys
import vacuum_environment as env
import neat
import pickle
import os

GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0


def play(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    pygame.init()
    start_time = pygame.time.get_ticks()
    clean = False
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((env.width, env.height))
    pygame.display.set_caption('Robot Vacuum AI')
    vacuum = env.Vacuum(display)
    font = pygame.font.Font(None, 54)
    font_color = pygame.Color('white')
    black = (0, 0, 0)

    while not clean:
        keys = pygame.key.get_pressed()
        display.blit(env.background, (0, 0))
        env.Vacuum.display(vacuum, vacuum.x, vacuum.y)

        """
        # Game controls
        if keys[pygame.K_UP]:
            vacuum.move()
        if keys[pygame.K_RIGHT]:
            vacuum.rotate_right()
        if keys[pygame.K_LEFT]:
            vacuum.rotate_left()
        """
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

        input = (vacuum.dir, vacuum.get_center(), env.calc_clean_percent(), vacuum.obstacle_detect())
        fitness = score + env.calc_clean_percent() * 100
        output = net.activate(input)

        if env.calc_clean_percent() >= .9 or passed_time / 1000 >= 20:
            print('Game Over. You scored ' + str(score) + ' points')
            print('Clean percentage: ' + str(env.calc_clean_percent() * 100))
            return fitness

        if output[0] > 0.5:
            vacuum.move()
        if output[1] > .5:
            vacuum.rotate_left()
        if output[2] > .5:
            vacuum.rotate_right()

        pygame.display.update()
        clock.tick(env.fps)


def eval_genomes(genomes, config):
    i = 0
    global SCORE
    global GENERATION, MAX_FITNESS, BEST_GENOME
    GENERATION += 1
    for genome_id, genome in genomes:

        genome.fitness = play(genome, config)
        print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f" % (GENERATION, i, genome.fitness, MAX_FITNESS))
        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
        SCORE = 0
        i += 1


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config')
pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
winner = pop.run(eval_genomes, 30)
print(winner)
outputDir = 'C:\\Users\\Corey\\PycharmProjects\\RoboVacAI\\bestGenomes'
os.chdir(outputDir)
serialNo = len(os.listdir(outputDir)) + 1
outputFile = open(str(serialNo) + '_' + str(int(MAX_FITNESS)) + '.p', 'wb')
pickle.dump(winner, outputFile)
