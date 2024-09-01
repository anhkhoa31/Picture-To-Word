import pygame
import sys
import random
import string
import time
import json
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1350
SCREEN_HEIGHT = 800

# Define size and spacing for letter boxes
box_size = 60  # Example size, adjust as needed
box_spacing = 10  # Example spacing, adjust as needed

# Define starting Y position for drawing word boxes
start_y = 400  # Y-coordinate for the starting position of word boxes

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Game Platform")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Colors for buttons
play_button_color = BLACK
play_button_hover_color = (50, 50, 50)  # Slightly lighter black for hover effect
play_button_text_color = WHITE

category_button_color = BLACK
category_button_hover_color = (50, 50, 50)  # Slightly lighter black for hover effect
category_button_text_color = WHITE

# Exit button color
exit_button_color = (205, 92, 92)
exit_button_hover_color = (240, 128, 128)

# Locked and completed stage colors
locked_stage_color = (169, 169, 169)
completed_stage_color = (144, 238, 144)  # Light Green color for completed stages

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
pixel_font = pygame.font.Font("pixel_font.ttf", 60)

# Game states
MAIN_MENU = "main_menu"
INTRO_SCENE = "intro_scene"
CATEGORY_SCENE = "category_scene"
STAGE_SELECTION = "stage_selection"
GAME_SCENE = "game_scene"
CONGRATS = "congrats"
current_state = MAIN_MENU

# Define selected category and other global variables
selected_category = None

# Timing and state tracking variables
incorrect_click_time = None  # Tracks the time of incorrect clicks
notification_duration = 2  # Duration to show notifications for incorrect clicks

# Create a dialog background surface
dialog_bg = pygame.Surface((1200, 300))
dialog_bg.fill((255, 255, 255, 128))  # Set a semi-transparent white background

# Categories and stages
categories = ["Easy", "Medium", "Hard"]
easy_stages = ["Dog", "Cat", "Bird", "Lion", "Elephant", "Giraffe", "Hedgehog"]
medium_stages = ["Entrepreneur", "Zeppelin", "Cathedral", "Mooring", "Cenotaph", "Quicksand", "Hippopotamus"]
hard_stages = ["Pomegranate", "Palanquin", "Antimacassar", "Kaleidoscope", "Astrolabe", "Sarcophagus"]

category_to_stages = {
    "Easy": easy_stages,
    "Medium": medium_stages,
    "Hard": hard_stages
}

# Define a mapping from categories to folder paths
category_folder_mapping = {
    "Easy": "Images/Easylevel",
    "Medium": "Images/Mediumlevel",
    "Hard": "Images/Hardlevel"
}

audio_folder_mapping = {
    "Easy": "Audio/Easylevel",
    "Medium": "Audio/Mediumlevel",
    "Hard": "Audio/Hardlevel"
}

# Initialize the unlocked stages dictionary
unlocked_stages = {
    "Easy": [True] + [False] * 6,  # Only the first stage is unlocked initially
    "Medium": [True] + [False] * 6,
    "Hard": [True] + [False] * 5   # Hard level has 6 stages
}

# Initialize the completed stages dictionary
completed_stages = {
    "Easy": [False] * 7,  # None of the stages are completed initially
    "Medium": [False] * 7,
    "Hard": [False] * 6
}

# JSON file to save and load the game state
SAVE_FILE = "game_save.json"

def load_game_progress():
    global completed_stages, unlocked_stages
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
            completed_stages = data.get("completed_stages", completed_stages)
            unlocked_stages = data.get("unlocked_stages", unlocked_stages)

def save_game_progress():
    data = {
        "completed_stages": completed_stages,
        "unlocked_stages": unlocked_stages
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)

# Load first map image
map_image = pygame.image.load("Images/new_map.jpg")  # First map (behind Tutor guy)
map_image = pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load second map image + resize
map_image2 = pygame.image.load("Images/map.jpg")  # Second map (Fade in)
map_image2 = pygame.transform.scale(map_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Tutor Guy image (tutorial character)
tutor_guy_image = pygame.image.load("Images/tutor_guy.png")
tutor_guy_rect = tutor_guy_image.get_rect()
tutor_guy_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Set Tutor Guy's initial position

# Define dialog text
dialog_text = [
    "HELLO PLAYER!",
    "WELCOME TO OUR GAME",
    "IT'S A PICTURE TO WORD GAME",
    "HOPE YOU LIKE IT..",
    "ENGLISH MIGHT BE HARD",
    "BUT IT'S FINE",
    "DON'T BE SCARED",
    "LET'S GO"
]

# Define button dimensions for stage selection
stage_button_width = 200
stage_button_height = 50

# Define the "Play" button
play_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 300, 200, 50))

# Define the "Exit" button
exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 400, 200, 50))

# Define the "Back" button
back_button_rect = pygame.Rect(10, 10, 100, 40)

# Define a button for switching to the character selection stage
character_selection_button_rect = pygame.Rect(150, 603, 600, 40)

# Define the "Audio" button
audio_button_width = 150
audio_button_height = 40
audio_button_x = SCREEN_WIDTH - audio_button_width - 20
audio_button_y = 10
audio_button_rect = pygame.Rect(audio_button_x, audio_button_y, audio_button_width, audio_button_height)

def play_bgm():
    pygame.mixer.music.load("Audio/BGM.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

def stop_bgm():
    pygame.mixer.music.stop()

def pause_bgm():
    pygame.mixer.music.pause()

def unpause_bgm():
    pygame.mixer.music.unpause()


# Define category buttons
category_button_width = 200
category_button_height = 50
category_buttons = [
    pygame.Rect((SCREEN_WIDTH - category_button_width) // 2, 200 + i * 80, category_button_width,
                category_button_height)
    for i in range(len(categories))
]
category_button_texts = [small_font.render(category, True, WHITE) for category in categories]

# Load and scale the common background image to fit the screen size
background_image = pygame.image.load("Images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()

stage_images = []
audio_files = []

def draw_main_menu():
    screen.fill(WHITE)
    if background_image:
        screen.blit(background_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # Draw the Play button
    if play_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, play_button_hover_color, play_button_rect)
    else:
        pygame.draw.rect(screen, play_button_color, play_button_rect)
    play_button_text = small_font.render("Play", True, play_button_text_color)
    screen.blit(play_button_text, (play_button_rect.x + (play_button_rect.width - play_button_text.get_width()) // 2,
                                   play_button_rect.y + (play_button_rect.height - play_button_text.get_height()) // 2))

    # Draw the Exit button
    if exit_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, exit_button_hover_color, exit_button_rect)
    else:
        pygame.draw.rect(screen, exit_button_color, exit_button_rect)
    exit_button_text = small_font.render("Exit", True, WHITE)
    screen.blit(exit_button_text, (exit_button_rect.x + (exit_button_rect.width - exit_button_text.get_width()) // 2,
                                   exit_button_rect.y + (exit_button_rect.height - exit_button_text.get_height()) // 2))

def draw_intro_scene():
    global current_state
    current_dialog_index = 0
    fade_out_alpha = 255

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle dialog progression with space key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_dialog_index += 1
                if current_dialog_index >= len(dialog_text):
                    running = False  # End the loop when dialogs are finished

        # Draw the background image based on the dialog state
        screen.blit(map_image if current_dialog_index < len(dialog_text) else map_image2, (0, 0))

        # Draw Tutor Guy only when dialog is active
        if current_dialog_index < len(dialog_text):
            screen.blit(tutor_guy_image, tutor_guy_rect)

            # Draw the dialog
            dialog_surface = pixel_font.render(dialog_text[current_dialog_index], True, (0, 0, 0))
            dialog_rect = dialog_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

            # Draw the dialog background
            screen.blit(dialog_bg, dialog_rect.move(0, -30))

            # Draw the dialog text
            screen.blit(dialog_surface, dialog_rect)

        pygame.display.flip()

    # Update the current state to transition to the category scene
    current_state = CATEGORY_SCENE

def draw_category_scene():
    screen.fill(WHITE)
    if background_image:
        screen.blit(background_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # Draw the Back button
    if back_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, exit_button_hover_color, back_button_rect)
    else:
        pygame.draw.rect(screen, exit_button_color, back_button_rect)
    back_button_text = small_font.render("Back", True, WHITE)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    # Calculate total height required for buttons
    total_height = len(category_buttons) * category_button_height + (len(category_buttons) - 1) * 20
    starting_y = (SCREEN_HEIGHT - total_height) // 2

    for i, rect in enumerate(category_buttons):
        rect.y = starting_y + i * (rect.height + 20)
        rect.x = (SCREEN_WIDTH - rect.width) // 2
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, category_button_hover_color, rect)
        else:
            pygame.draw.rect(screen, category_button_color, rect)
        screen.blit(category_button_texts[i], (rect.x + (rect.width - category_button_texts[i].get_width()) // 2,
                                               rect.y + (rect.height - category_button_texts[i].get_height()) // 2))

    pygame.display.flip()

def draw_stage_selection():
    screen.fill(WHITE)
    if background_image:
        screen.blit(background_image, (0, 0))

    # Draw the Back button
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, exit_button_hover_color, back_button_rect)
    else:
        pygame.draw.rect(screen, exit_button_color, back_button_rect)
    back_button_text = small_font.render("Back", True, WHITE)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    total_height = len(stage_buttons) * stage_buttons[0].height + (len(stage_buttons) - 1) * 20
    starting_y = (SCREEN_HEIGHT - total_height) // 2 + 50

    for i, rect in enumerate(stage_buttons):
        rect.y = starting_y + i * (rect.height + 20)
        rect.x = (SCREEN_WIDTH - rect.width) // 2

        # Determine the stage color based on its status (completed, unlocked, or locked)
        if completed_stages[selected_category][i]:
            stage_color = completed_stage_color  # Light Green for completed stages
        elif unlocked_stages[selected_category][i]:
            stage_color = play_button_color
        else:
            stage_color = locked_stage_color  # Grey for locked stages

        if unlocked_stages[selected_category][i] or completed_stages[selected_category][i]:
            if rect.collidepoint(mouse_pos) and not completed_stages[selected_category][i]:
                pygame.draw.rect(screen, play_button_hover_color, rect)
            else:
                pygame.draw.rect(screen, stage_color, rect)
            screen.blit(stage_button_texts[i], (rect.x + (rect.width - stage_button_texts[i].get_width()) // 2,
                                                rect.y + (rect.height - stage_button_texts[i].get_height()) // 2))
        else:  # Stage is locked
            pygame.draw.rect(screen, locked_stage_color, rect)
            locked_text = small_font.render(f"Stage {i + 1}", True, WHITE)
            screen.blit(locked_text, (rect.x + (rect.width - locked_text.get_width()) // 2,
                                      rect.y + (rect.height - locked_text.get_height()) // 2))

def handle_stage_selection(stage_index):
    global current_stage, word_to_guess, guessed_word, correctly_clicked_letters, current_state
    global all_letters, rows, score

    current_stage = stage_index
    word_to_guess = stages[current_stage].upper()

    # Initialize score for the stage
    score = 0

    guessed_word = ["_" for _ in word_to_guess]
    correctly_clicked_letters = []

    additional_letters = random.sample(string.ascii_uppercase, 5)
    all_letters = list(word_to_guess.upper()) + additional_letters
    random.shuffle(all_letters)

    rows = [all_letters[i:i + 5] for i in range(0, len(all_letters), 5)]

    current_state = GAME_SCENE

def draw_game_scene():
    global current_stage, incorrect_click_time, score

    screen.blit(background_image, (0, 0))

    if 0 <= current_stage < len(stage_images):
        stage_image = stage_images[current_stage]
        x = (SCREEN_WIDTH - stage_image.get_width()) // 2
        y = (SCREEN_HEIGHT - stage_image.get_height()) // 2 - 200
        screen.blit(stage_image, (x, y))

    # Draw the Back button
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, exit_button_hover_color, back_button_rect)
    else:
        pygame.draw.rect(screen, exit_button_color, back_button_rect)
    back_button_text = small_font.render("Back", True, WHITE)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    # Draw the Audio button
    if audio_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, play_button_hover_color, audio_button_rect)
    else:
        pygame.draw.rect(screen, play_button_color, audio_button_rect)
    audio_button_text = small_font.render("Play Audio", True, WHITE)
    screen.blit(audio_button_text, (audio_button_rect.x + (audio_button_rect.width - audio_button_text.get_width()) // 2,
                 audio_button_rect.y + (audio_button_rect.height - audio_button_text.get_height()) // 2))

    draw_word_boxes()
    draw_letter_boxes()

    if incorrect_click_time:
        current_time = time.time()
        if current_time - incorrect_click_time < notification_duration:
            show_incorrect_click_notification()
        else:
            incorrect_click_time = None
    if "_" not in guessed_word:
        score += 50  # Example: Award 50 points for winning
        current_state = CONGRATS
        show_congrats_message()

def draw_word_boxes():
    total_width = len(guessed_word) * (box_size + box_spacing) - box_spacing
    start_x = (SCREEN_WIDTH - total_width) // 2
    for i, letter in enumerate(guessed_word):
        x = start_x + i * (box_size + box_spacing)
        pygame.draw.rect(screen, WHITE, (x, start_y, box_size, box_size), 0)
        pygame.draw.rect(screen, BLACK, (x, start_y, box_size, box_size), 2)
        if letter != "_":
            letter_surface = font.render(letter, True, BLACK)
            screen.blit(letter_surface, (
                x + (box_size - letter_surface.get_width()) // 2,
                start_y + (box_size - letter_surface.get_height()) // 2))

def draw_letter_boxes():
    for row_idx, row in enumerate(rows):
        row_start_x = (SCREEN_WIDTH - (box_size + box_spacing) * len(row)) // 2
        y = start_y + 100 + row_idx * (box_size + box_spacing)
        for i, letter in enumerate(row):
            if letter not in correctly_clicked_letters:
                x = row_start_x + i * (box_size + box_spacing)
                pygame.draw.rect(screen, WHITE, (x, y, box_size, box_size), 0)
                pygame.draw.rect(screen, BLACK, (x, y, box_size, box_size), 2)
                letter_surface = font.render(letter, True, BLACK)
                screen.blit(letter_surface, (
                    x + (box_size - letter_surface.get_width()) // 2,
                    y + (box_size - letter_surface.get_height()) // 2))

def show_congrats_message():
    global current_state

    popup_width, popup_height = 1000, 500
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2

    popup_color = (255, 255, 224)  # LIGHT_YELLOW
    border_color = BLACK

    pygame.draw.rect(screen, popup_color, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, border_color, (popup_x, popup_y, popup_width, popup_height), 2)

    message = font.render("Congrats! You found the word!", True, BLACK)
    screen.blit(message, (popup_x + (popup_width - message.get_width()) // 2, popup_y + 50))

    word_reveal = small_font.render(f"The word is: {word_to_guess}", True, BLACK)
    screen.blit(word_reveal, (popup_x + (popup_width - word_reveal.get_width()) // 2, popup_y + 150))

    button_width, button_height = 200, 50
    button_x = popup_x + (popup_width - button_width) // 2
    button_y = popup_y + popup_height - button_height - 30
    pygame.draw.rect(screen, BLUE, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)
    button_text = small_font.render("Continue", True, WHITE)
    screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2,
                              button_y + (button_height - button_text.get_height()) // 2))

    completed_stages[selected_category][current_stage] = True

    if current_stage + 1 < len(unlocked_stages[selected_category]):
        unlocked_stages[selected_category][current_stage + 1] = True

    save_game_progress()

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    waiting = False
                    break
        pygame.time.delay(100)

    current_state = STAGE_SELECTION


def handle_mouse_click(x, y):
    global current_state, selected_category, stage_buttons, stage_button_texts
    global stage_images, audio_files, stages, incorrect_click_time, correctly_clicked_letters, guessed_word

    if current_state == MAIN_MENU:
        if play_button_rect.collidepoint(x, y):
            current_state = INTRO_SCENE
            play_bgm()
        elif exit_button_rect.collidepoint(x, y):
            save_game_progress()
            stop_bgm()
            pygame.quit()
            sys.exit()

    elif current_state == INTRO_SCENE:
        pass

    elif current_state == CATEGORY_SCENE:
        if back_button_rect.collidepoint(x, y):
            current_state = MAIN_MENU
        else:
            for i, rect in enumerate(category_buttons):
                if rect.collidepoint(x, y):
                    selected_category = categories[i]

                    stages = category_to_stages[selected_category]
                    image_folder_path = category_folder_mapping[selected_category]
                    audio_folder_path = audio_folder_mapping[selected_category]

                    stage_buttons = [
                        pygame.Rect((SCREEN_WIDTH - stage_button_width) // 2, 200 + j * 80, stage_button_width,
                                    stage_button_height)
                        for j in range(len(stages))
                    ]
                    stage_button_texts = [small_font.render(f"Stage {j + 1}", True, WHITE) for j in range(len(stages))]

                    stage_images = [
                        pygame.image.load(f"{image_folder_path}/stage{i + 1}.jpg").convert_alpha()
                        for i in range(len(stages))
                    ]

                    audio_files = [
                        pygame.mixer.Sound(f"{audio_folder_path}/stage{i + 1}.wav")
                        for i in range(len(stages))
                    ]

                    current_state = STAGE_SELECTION
                    break

    elif current_state == STAGE_SELECTION:
        if back_button_rect.collidepoint(x, y):
            current_state = CATEGORY_SCENE
        else:
            for i, rect in enumerate(stage_buttons):
                if rect.collidepoint(x, y) and (unlocked_stages[selected_category][i] or completed_stages[selected_category][i]):
                    handle_stage_selection(i)

    elif current_state == GAME_SCENE:
        if back_button_rect.collidepoint(x, y):
            current_state = STAGE_SELECTION
        elif audio_button_rect.collidepoint(x, y):
            if 0 <= current_stage < len(audio_files):
                pause_bgm()
                time.sleep(0)
                audio_files[current_stage].play()
                unpause_bgm()
        else:
            for row_idx, row in enumerate(rows):
                row_start_x = (SCREEN_WIDTH - (box_size + box_spacing) * len(row)) // 2
                box_y = start_y + 100 + row_idx * (box_size + box_spacing)
                for i, letter in enumerate(row):
                    box_x = row_start_x + i * (box_size + box_spacing)
                    if box_x < x < box_x + box_size and box_y < y < box_y + box_size:
                        letter = letter.upper()
                        if letter in word_to_guess.upper() and letter not in correctly_clicked_letters:
                            correctly_clicked_letters.append(letter)
                            for idx, char in enumerate(word_to_guess.upper()):
                                if char == letter:
                                    guessed_word[idx] = letter
                            if "_" not in guessed_word:
                                current_state = CONGRATS
                                show_congrats_message()
                        else:
                            incorrect_click_time = time.time()  # Set this when an incorrect click is detected
                        return letter
    return None

def show_incorrect_click_notification():
    notification_text = small_font.render("You chose the wrong letter", True, RED)
    screen.blit(notification_text, (SCREEN_WIDTH // 2 - notification_text.get_width() // 2, SCREEN_HEIGHT - 100))

# Load game progress when the game starts
load_game_progress()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_progress()
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_state == CONGRATS:
                if event.key == pygame.K_RETURN:
                    current_state = MAIN_MENU
                    guessed_word = ["_" for _ in word_to_guess]
                    correctly_clicked_letters.clear()
                    incorrect_click_time = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            handle_mouse_click(mouse_x, mouse_y)

    if current_state == MAIN_MENU:
        draw_main_menu()
    elif current_state == INTRO_SCENE:
        draw_intro_scene()
    elif current_state == CATEGORY_SCENE:
        draw_category_scene()
    elif current_state == STAGE_SELECTION:
        draw_stage_selection()
    elif current_state == GAME_SCENE:
        draw_game_scene()
    elif current_state == CONGRATS:
        show_congrats_message()

    pygame.display.flip()

pygame.quit()
sys.exit()