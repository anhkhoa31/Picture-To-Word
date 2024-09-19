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
LIGHT_YELLOW = (255, 255, 224)
GOLD = (255, 223, 0)
GREY = (200, 200, 200)
DARK_GREY = (169, 169, 169)

# Colors for buttons
play_button_color = BLACK
play_button_hover_color = (50, 50, 50)
play_button_text_color = WHITE

category_button_color = BLACK
category_button_hover_color = (50, 50, 50)
category_button_text_color = WHITE

# Exit button color
exit_button_color = (205, 92, 92)
exit_button_hover_color = (240, 128, 128)

# Locked and completed stage colors
locked_stage_color = (169, 169, 169)
completed_stage_color = (144, 238, 144)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
pixel_font = pygame.font.Font("pixel_font.ttf", 60)
daily_reward_font = pygame.font.Font(None, 24)

# Game states
MAIN_MENU = "main_menu"
INTRO_SCENE = "intro_scene"
CATEGORY_SCENE = "category_scene"
STAGE_SELECTION = "stage_selection"
GAME_SCENE = "game_scene"
CONGRATS = "congrats"
current_state = MAIN_MENU # Showing the main menu whenever the program runs

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
    "Easy": [True] + [False] * 6,  # Only the first stage is unlocked in the beginning
    "Medium": [True] + [False] * 6,
    "Hard": [True] + [False] * 5
}

# Initialize the completed stages dictionary
completed_stages = {
    "Easy": [False] * 7,  # None of the stages are completed in the beginning
    "Medium": [False] * 7,
    "Hard": [False] * 6
}

# Daily reward setup -----------------
# Reward setup
gems_per_day = [100 * (i + 1) for i in range(7)]
total_gems = 0

# Track which days have been claimed
claimed_days = [False] * 7

# Timer setup (5 seconds = 1 day)
start_time = time.time()
current_day = 0

# Frame size and position
frame_width = SCREEN_WIDTH * 0.8
frame_height = SCREEN_HEIGHT * 0.42
frame_x = (SCREEN_WIDTH - frame_width) / 2
frame_y = (SCREEN_HEIGHT - frame_height) / 2

# Number of day boxes on top and bottom
num_boxes_top = 4
num_boxes_bottom = 3

# Margins and spacing
margin = 10
spacing = 20

# Calculate box size
available_height = frame_height * 1.4 - spacing
box_height = (available_height - (num_boxes_bottom - 1) * margin) / num_boxes_bottom
box_width = (frame_width - (num_boxes_top + 1) * margin) / num_boxes_top

# Gem icon
gem_icon_image = pygame.image.load("Images/Icon/gem_icon.png")
gem_icon_size = 24
gem_icon_image = pygame.transform.scale(gem_icon_image, (gem_icon_size, gem_icon_size))

# Reward icon
icon_image = pygame.image.load("Images/Icon/gift_icon.png")
icon_image = pygame.transform.scale(icon_image, (gem_icon_size, gem_icon_size))

# Reward icon position
icon_y = 20

# Track if the reward frame is visible
show_reward_frame = False

# JSON file to save and load the game state
SAVE_FILE = "game_save.json"


def load_game_progress():
    global completed_stages, unlocked_stages
    # Check the save_file if it exists
    if os.path.exists(SAVE_FILE):
        # If it already exists open the file in read mode
        with open(SAVE_FILE, "r") as file:
            # Load the file
            data = json.load(file)
            completed_stages = data.get("completed_stages", completed_stages)
            unlocked_stages = data.get("unlocked_stages", unlocked_stages)


def save_game_progress():
    # Save the data using dictionary data type
    data = {
        "completed_stages": completed_stages,
        "unlocked_stages": unlocked_stages
    }
    # open the file in write mode
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
audio_button_rect = pygame.Rect(SCREEN_WIDTH - 170, 10, 150, 40)

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
# Adjusting the position of the category buttons
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

    # Place the image in the top left corner X: 0 and Y: 0
    screen.blit(background_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # Draw the Play button
    # Change color if the pointer is inside the rectangular defined area
    if play_button_rect.collidepoint(mouse_pos):
        # If the pointer is on the button change to hover color
        pygame.draw.rect(screen, play_button_hover_color, play_button_rect)
    else:
        # If the pointer is not on the button use the pre-defined color
        pygame.draw.rect(screen, play_button_color, play_button_rect)
    play_button_text = small_font.render("Play", True, play_button_text_color)

    # Place the text in the center of the button
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

    # Draw daily reward system if applicable
    if show_reward_frame:
        pygame.draw.rect(screen, GREY, (frame_x, frame_y, frame_width, frame_height), 2)
        for i in range(num_boxes_top):
            x = frame_x + (i * (box_width + margin)) + margin
            y = frame_y + spacing
            box_color = DARK_GREY if claimed_days[i] else GOLD
            pygame.draw.rect(screen, box_color, (x, y, box_width, box_height))
            day_text = daily_reward_font.render(f"Day {i + 1}", True, BLACK)
            day_text_rect = day_text.get_rect(center=(x + box_width / 2, y + box_height / 2 - 10))
            screen.blit(day_text, day_text_rect)
            reward_text = daily_reward_font.render(f"{gems_per_day[i]}", True, BLACK)
            gem_icon_x = x + (box_width - gem_icon_size - reward_text.get_width()) / 2
            gem_icon_y = y + box_height / 2
            screen.blit(gem_icon_image, (gem_icon_x, gem_icon_y - 3))
            reward_text_rect = reward_text.get_rect(
                center=(gem_icon_x + gem_icon_size + reward_text.get_width() / 2, gem_icon_y + 10))
            screen.blit(reward_text, reward_text_rect)
        for i in range(num_boxes_bottom):
            x = frame_x + (i * (box_width + margin)) + margin
            y = frame_y + box_height + spacing * 2
            box_color = DARK_GREY if claimed_days[num_boxes_top + i] else GOLD
            pygame.draw.rect(screen, box_color, (x, y, box_width, box_height))
            day_text = daily_reward_font.render(f"Day {num_boxes_top + i + 1}", True, BLACK)
            day_text_rect = day_text.get_rect(center=(x + box_width / 2, y + box_height / 2 - 10))
            screen.blit(day_text, day_text_rect)
            reward_text = daily_reward_font.render(f"{gems_per_day[num_boxes_top + i]}", True, BLACK)
            gem_icon_x = x + (box_width - gem_icon_size - reward_text.get_width()) / 2
            gem_icon_y = y + box_height / 2
            screen.blit(gem_icon_image, (gem_icon_x, gem_icon_y - 3))
            reward_text_rect = reward_text.get_rect(
                center=(gem_icon_x + gem_icon_size + reward_text.get_width() / 2, gem_icon_y + 10))
            screen.blit(reward_text, reward_text_rect)

    # Draw the gem icon, total gems, and reward icon
    total_gems_text = small_font.render(f"{total_gems}", True, GOLD)
    total_gems_width = total_gems_text.get_width()
    gem_icon_x = SCREEN_WIDTH - 20 - gem_icon_size - total_gems_width - 10 - gem_icon_size - 10
    total_gems_x = gem_icon_x + gem_icon_size + 5
    global icon_x
    icon_x = total_gems_x + total_gems_width + 10
    screen.blit(gem_icon_image, (gem_icon_x, icon_y))
    total_gems_rect = total_gems_text.get_rect(midleft=(total_gems_x, icon_y + gem_icon_size / 2))
    screen.blit(total_gems_text, total_gems_rect)
    screen.blit(icon_image, (icon_x, icon_y))


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

    # Set the gap for all buttons
    total_height = len(category_buttons) * category_button_height + (len(category_buttons) - 1) * 20
    starting_y = (SCREEN_HEIGHT - total_height) // 2

    for i, rect in enumerate(category_buttons):
        # For each category button it has 20 pixels space between them
        rect.y = starting_y + i * (rect.height + 20)
        # Place all buttons in the center of the screen
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

        # Apply color for completed stage, locked stage and unlocked stage
        if completed_stages[selected_category][i]:
            stage_color = completed_stage_color
        elif unlocked_stages[selected_category][i]:
            stage_color = play_button_color
        else:
            stage_color = locked_stage_color

        # Check if the current stage is unlocked or completed
        if unlocked_stages[selected_category][i] or completed_stages[selected_category][i]:
            # If the mouse is hovering over a stage which is not completed change the color of unlocked stage
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
    # Give access to these variables outside this function
    global current_stage, word_to_guess, guessed_word, correctly_clicked_letters, current_state
    global all_letters, rows, score

    current_stage = stage_index

    # Set up the word to guess
    # The words for each stage are defined earlier
    # Convert the word to uppercase to avoid case conflict
    word_to_guess = stages[current_stage].upper()

    # Create an array of the guessed_word by replacing each letter in the word_to_guess with " _ "
    # The " _ " will be replaced with the correct guessed letter
    guessed_word = ["_" for _ in word_to_guess]

    # This array is used to store the correct word of a player
    correctly_clicked_letters = []

    # Randomly choose 5 words which are not a part of the word_to_guessed
    additional_letters = random.sample(string.ascii_uppercase, 5)

    # Combine the word_to_guess with the additional_letters
    all_letters = list(word_to_guess.upper()) + additional_letters

    # Shuffle the list so it appears randomly
    random.shuffle(all_letters)

    # A row only contains 5 boxes of letters
    rows = [all_letters[i:i + 5] for i in range(0, len(all_letters), 5)]

    # Set the current stage to game_scene which is the final stage of the project
    current_state = GAME_SCENE


def draw_game_scene():
    global current_stage, incorrect_click_time, score

    screen.blit(background_image, (0, 0))

    # Determine which stage image to display na dit must be in the stage limit
    if 0 <= current_stage < len(stage_images):
        stage_image = stage_images[current_stage]
        x = (SCREEN_WIDTH - stage_image.get_width()) // 2

        # Ensure the stage height will not be covered by the platform screen
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
    screen.blit(audio_button_text,
                (audio_button_rect.x + (audio_button_rect.width - audio_button_text.get_width()) // 2,
                 audio_button_rect.y + (audio_button_rect.height - audio_button_text.get_height()) // 2))

    draw_word_boxes()
    draw_letter_boxes()

    if incorrect_click_time:
        # Retrieve the current time in seconds since this case happens
        current_time = time.time()

        # Calculate the time difference between the current time and the incorrect_click_time
        # The notification will be visible the result is less than the notification duration
        if current_time - incorrect_click_time < notification_duration:
            show_incorrect_click_notification()
        else:
            incorrect_click_time = None

    # Check the guess_word if there is no underscore, it means that the word is fully guessed
    if "_" not in guessed_word:
        # Show congrats message
        current_state = CONGRATS
        show_congrats_message()


def draw_word_boxes():
    # Ensure that every box has the same box_size and same space between them
    # " - box_spacing" is for the last box since there is the box behind it
    total_width = len(guessed_word) * (box_size + box_spacing) - box_spacing

    # Ensure the box is centered
    start_x = (SCREEN_WIDTH - total_width) // 2

    # For each letter or underscore, position the box according to the calculated x-coordinate
    for i, letter in enumerate(guessed_word):
        x = start_x + i * (box_size + box_spacing)

        # Draw the box and placed in the calculated coordinate
        # Filled the box with white background
        pygame.draw.rect(screen, WHITE, (x, start_y, box_size, box_size), 0)
        # Using black color for the letter
        pygame.draw.rect(screen, BLACK, (x, start_y, box_size, box_size), 2)

        # If the letter is underscore, leave the box empty
        if letter != "_":
            # Filling the letter using this font
            letter_surface = font.render(letter, True, BLACK)
            # Draw the letter onto the screen
            screen.blit(letter_surface, (
                # Display the letter in the center of the box
                x + (box_size - letter_surface.get_width()) // 2,
                start_y + (box_size - letter_surface.get_height()) // 2))


def draw_letter_boxes():
    # Loop through draw boxes for letter based on calculated size and spacing
    for row_idx, row in enumerate(rows):
        # Calculate the x and y coordinate of all boxes combined
        row_start_x = (SCREEN_WIDTH - (box_size + box_spacing) * len(row)) // 2
        y = start_y + 100 + row_idx * (box_size + box_spacing)
        # Loop through the index of letters in the row
        for i, letter in enumerate(row):
            if letter not in correctly_clicked_letters:
                # Calculate the position of each box in the row
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

    popup_color = (255, 255, 224)
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

    # Whenever a congratulatory message shows up mark the current stage as completed
    completed_stages[selected_category][current_stage] = True

    # Unlock the next stage
    if current_stage + 1 < len(unlocked_stages[selected_category]):
        unlocked_stages[selected_category][current_stage + 1] = True

    save_game_progress()

    pygame.display.flip()

    # While true loop
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check if the user click on the "continue" button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the cursor at the time it pressed
                mouse_x, mouse_y = event.pos
                # Ensure that the cursor position when it is clicked within the "continue" button
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    waiting = False
                    break

    current_state = STAGE_SELECTION


def handle_mouse_click(x, y):
    global current_state, selected_category, stage_buttons, stage_button_texts
    global stage_images, audio_files, stages, incorrect_click_time, correctly_clicked_letters, guessed_word
    global show_reward_frame, claimed_days, total_gems, start_time, current_day

    if current_state == MAIN_MENU:
        # If player clicks on the play button in the main menu
        # Move to the intro scene and play background music
        if play_button_rect.collidepoint(x, y):
            current_state = INTRO_SCENE
            play_bgm()
        # If the exit button is pressed, save and exit the game
        elif exit_button_rect.collidepoint(x, y):
            save_game_progress()
            stop_bgm()
            pygame.quit()
            sys.exit()
        # Handle Reward icon click
        elif icon_x < x < icon_x + gem_icon_size and icon_y < y < icon_y + gem_icon_size:
            show_reward_frame = not show_reward_frame  # Toggle reward frame visibility
        # Handle clicking outside the reward frame
        elif show_reward_frame:
            if not (frame_x < x < frame_x + frame_width and frame_y < y < frame_y + frame_height):
                show_reward_frame = False  # Hide reward frame
        # Handle daily reward boxes click
        if show_reward_frame:
            # Check if a box on the top row was clicked
            for i in range(num_boxes_top):
                if i > current_day:  # Prevent claiming future days
                    continue
                x_box = frame_x + (i * (box_width + margin)) + margin
                y_box = frame_y + spacing
                if x_box < x < x_box + box_width and y_box < y < y_box + box_height:
                    if not claimed_days[i]:  # Check if the reward hasn't been claimed
                        claimed_days[i] = True
                        total_gems += gems_per_day[i]

            # Check if a box on the bottom row was clicked
            for i in range(num_boxes_bottom):
                if num_boxes_top + i > current_day:  # Prevent claiming future days
                    continue
                x_box = frame_x + (i * (box_width + margin)) + margin
                y_box = frame_y + box_height + spacing * 2
                if x_box < x < x_box + box_width and y_box < y < y_box + box_height:
                    if not claimed_days[num_boxes_top + i]:  # Check if the reward hasn't been claimed
                        claimed_days[num_boxes_top + i] = True
                        total_gems += gems_per_day[num_boxes_top + i]

    # Don't need to get any action from the mouse since the intro scene take the spacebars as input
    elif current_state == INTRO_SCENE:
        pass

    elif current_state == CATEGORY_SCENE:
        # If the back button is clicked brings user back to the main menu
        if back_button_rect.collidepoint(x, y):
            current_state = MAIN_MENU
        else:
            for i, rect in enumerate(category_buttons):
                if rect.collidepoint(x, y):
                    # Open the associated level with the button that is clicked
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
                if rect.collidepoint(x, y) and (
                        unlocked_stages[selected_category][i] or completed_stages[selected_category][i]):
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
                # Placing the row of boxes both horizontally and vertically in the middle
                row_start_x = (SCREEN_WIDTH - (box_size + box_spacing) * len(row)) // 2
                box_y = start_y + 100 + row_idx * (box_size + box_spacing)
                for i, letter in enumerate(row):
                    # Setting position of each box in the row
                    box_x = row_start_x + i * (box_size + box_spacing)
                    # Check the click if it is within the box size
                    if box_x < x < box_x + box_size and box_y < y < box_y + box_size:
                        letter = letter.upper()
                        # Check if the clicked word is in the word to guess also check if it was not clicked
                        if letter in word_to_guess.upper() and letter not in correctly_clicked_letters:
                            # Add the correct clicked word to the list
                            correctly_clicked_letters.append(letter)
                            for idx, char in enumerate(word_to_guess.upper()):
                                # Update the guessed word list to show the correct letter
                                if char == letter:
                                    guessed_word[idx] = letter
                            # If all letters have been guessed show the congrats message
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
    elapsed_time = time.time() - start_time
    current_day = min(7, int(elapsed_time // 5))

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