import pygame
import random

# Initialize pygame
pygame.init()

# Set display
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 5
CLOWN_ACCELERATION = 1
CENTER = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2

# Set variables
score = 0
player_lives = PLAYER_STARTING_LIVES
clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Colors
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)

# Set font
font = pygame.font.Font("assets/Franxurter.ttf", 32)

# Set text for title (similar to score)
title_text = font.render("Catch the Clown: ", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

# Set text for score
score_text = font.render("Score: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)

# Set text for lives
lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

# Set text for game over
game_over_text = font.render("GAMEOVER", True, BLUE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2

# Set text for continue
continue_text = font.render("Press any key to play again", True, YELLOW)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2 + 230, WINDOW_HEIGHT // 2 + 64)

# Load clown image
clown_image = pygame.image.load("assets/clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = CENTER

# Load backround image
background_image = pygame.image.load("assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Load sound effects
pygame.mixer.music.load("assets/ctc_background_music.wav")
click_sound = pygame.mixer.Sound("assets/click_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while (previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            # We missed the clown
            else:
                miss_sound.play()
                player_lives -= 1

    # Update game state
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # Reverse direction if the clown hits the screen edges
    if clown_rect.right >= WINDOW_WIDTH or clown_rect.left <= 0:
        clown_dx = -clown_dx  # Reverse horizontal direction
    if clown_rect.bottom >= WINDOW_HEIGHT or clown_rect.top <= 0:
        clown_dy = -clown_dy  # Reverse vertical direction

    # Update the HUD
    score_text = font.render(f"Score: {score}", True, YELLOW)
    lives_text = font.render(f"Lives: {player_lives}", True, YELLOW)

    # Check for Game Over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player clicks then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to play again.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    clown_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Blit HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)

    # Blit assets
    display_surface.blit(clown_image, clown_rect)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

    # Exit the game
pygame.quit()