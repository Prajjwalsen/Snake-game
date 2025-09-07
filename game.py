author = 'Prajjwal'

#Importing The Modules
import pygame
import random
import os

#Initialization
pygame.mixer.init()
pygame.init()


#Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
snakegreen = (35, 45, 40)

#Creating The window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Backgrounds
bg1 = pygame.image.load("Screen/bg1.jpg")  # Welcome screen
bg1 = pygame.transform.scale(bg1, (screen_width, screen_height))

bg_game = pygame.image.load("Screen/bg.png")  # Game playing background
bg_game = pygame.transform.scale(bg_game, (screen_width, screen_height))

outro = pygame.image.load("Screen/bg2.jpg")  # Game over background
outro = pygame.transform.scale(outro, (screen_width, screen_height))


#Game Title
pygame.display.set_caption("Snake By Prajjwal")
pygame.display.update()

#Music
pygame.mixer.music.load('music/wc.mp3')
pygame.mixer.music.play(100)
pygame.mixer.music.set_volume(.6)

#Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)

def text_screen(text, color, x, y):
   screen_text = font.render(text, True, color)
   gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
   for x,y in snk_list:
       pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


#Welcome Screen

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(bg1, (0, 0))  # Use bg1 as the welcome screen background

        # Draw prompt text in center
        text_screen("Press ENTER to Play", white, screen_width // 2 - 150, screen_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('music/bgm.mp3')
                    pygame.mixer.music.play(100)
                    pygame.mixer.music.set_volume(.6)
                    gameloop()

        pygame.display.update()
        clock.tick(60)

    

# Game Loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.blit(outro, (0, 0))

            # Score text placed below Game Over text to avoid overlap
            text_screen("Score: " + str(score), white, screen_width // 2 - 60, screen_height - 70)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.blit(bg_game, (0, 0))  # Gameplay background
            text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), snakegreen, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1] or snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('music/bgm1.mp3')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.6)

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()