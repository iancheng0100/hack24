import pygame
import pygame_gui
import sys
import main_game

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game of Growth")

# Create a UI manager for pygame_gui with a custom theme
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

# Set background color to black
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

score_max = 0

# Center title "Game of Growth"
title_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 300), (400, 70)),
    text="Game of Growth",
    manager=ui_manager,
    object_id="#title_label"
)

# score
score_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 500), (400, 70)),
    text=f"Highest score: {score_max}",
    manager=ui_manager,
    object_id="#score_label"
)

# Create "Play" button in the center below the title
play_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 400), (200, 50)),
    text="Play",
    manager=ui_manager,
    object_id="#play_button"
)

# Create "Achievements" button in the top right corner
achievements_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((600, 20), (180, 50)),
    text="Achievements",
    manager=ui_manager,
    object_id="#achievements_button"
)

# Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Process UI events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    score = main_game.main()
                    score_max = max(score, score_max)
                    score_label.set_text(f"Highest score: {score_max}")
                if event.ui_element == achievements_button:
                    print("Achievements button clicked!")

        # Handle UI manager events
        ui_manager.process_events(event)

    # Fill screen with black
    screen.fill(BLACK)

    # Update the UI manager
    ui_manager.update(time_delta)

    # Draw the UI elements
    ui_manager.draw_ui(screen)

    # Update display
    pygame.display.flip()
