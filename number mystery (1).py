import pygame
import random
import math
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NUMBER MYSTERY")

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("arial", 64, bold=True)
heading_font = pygame.font.SysFont("arial", 32, bold=True)
font = pygame.font.SysFont("arial", 25, bold=True)
small_font = pygame.font.SysFont("arial", 18)

# Colors
BG = (9, 10, 30)
WHITE = (245, 245, 255)
CYAN = (30, 220, 255)
PURPLE = (150, 70, 255)
PINK = (255, 70, 160)
GREEN = (50, 255, 150)
RED = (255, 75, 90)
GRAY = (150, 160, 190)
PANEL = (22, 25, 60)

# Game states
MENU = "menu"
PLAYING = "playing"
RESULT = "result"

state = MENU

# Difficulty settings
difficulties = {
    "EASY": (1, 50, 10),
    "MEDIUM": (1, 100, 10),
    "HARD": (1, 500, 12)
}

difficulty = "MEDIUM"
secret_number = 0
attempts = 0
max_attempts = 10
score = 0
guess_text = ""
message = "ENTER YOUR GUESS!"
message_color = CYAN
history = []
result_message = ""

# Background particles
particles = [
    [random.randint(0, WIDTH),
     random.randint(0, HEIGHT),
     random.randint(1, 3),
     random.uniform(0.3, 1.2)]
    for _ in range(90)
]


def draw_background():
    screen.fill(BG)

    # Moving particles
    for p in particles:
        p[1] -= p[3]

        if p[1] < 0:
            p[1] = HEIGHT
            p[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (60, 65, 120),
            (int(p[0]), int(p[1])),
            p[2]
        )

    # Decorative circles
    pygame.draw.circle(
        screen, (20, 25, 65), (80, 100), 150, 2
    )
    pygame.draw.circle(
        screen, (35, 20, 75), (920, 550), 180, 2
    )


def draw_text(text, fnt, color, x, y, center=True):
    image = fnt.render(str(text), True, color)

    if center:
        rect = image.get_rect(center=(x, y))
    else:
        rect = image.get_rect(topleft=(x, y))

    screen.blit(image, rect)
    return rect


def draw_button(text, rect, color, mouse_pos):
    hovering = rect.collidepoint(mouse_pos)

    button_color = tuple(
        min(255, c + 35) for c in color
    ) if hovering else color

    # Glow effect
    glow = pygame.Rect(
        rect.x - 4, rect.y - 4,
        rect.width + 8, rect.height + 8
    )

    pygame.draw.rect(
        screen, (35, 45, 90), glow,
        border_radius=16
    )

    pygame.draw.rect(
        screen, button_color, rect,
        border_radius=13
    )

    pygame.draw.rect(
        screen, WHITE, rect,
        2, border_radius=13
    )

    draw_text(
        text, font, WHITE,
        rect.centerx, rect.centery
    )

    return hovering


def start_game():
    global secret_number, attempts, max_attempts
    global score, guess_text, message, message_color
    global history, state, result_message

    low, high, max_attempts = difficulties[difficulty]

    secret_number = random.randint(low, high)
    attempts = 0
    score = 0
    guess_text = ""
    history = []
    message = f"GUESS A NUMBER FROM {low} TO {high}"
    message_color = CYAN
    result_message = ""

    state = PLAYING


def check_guess():
    global attempts, score, guess_text
    global message, message_color, state
    global result_message

    if not guess_text.isdigit():
        message = "PLEASE ENTER A VALID NUMBER!"
        message_color = RED
        return

    guess = int(guess_text)

    low, high, _ = difficulties[difficulty]

    if guess < low or guess > high:
        message = f"ENTER BETWEEN {low} AND {high}!"
        message_color = RED
        guess_text = ""
        return

    attempts += 1
    history.append(guess)

    if guess == secret_number:
        score = 100 + (max_attempts - attempts) * 20
        result_message = "YOU SOLVED THE MYSTERY!"
        state = RESULT

    elif attempts >= max_attempts:
        result_message = "YOU RAN OUT OF ATTEMPTS!"
        state = RESULT

    elif guess < secret_number:
        message = "TOO LOW! TRY A HIGHER NUMBER"
        message_color = PINK

    else:
        message = "TOO HIGH! TRY A LOWER NUMBER"
        message_color = RED

    guess_text = ""


# Buttons
easy_btn = pygame.Rect(190, 390, 190, 60)
medium_btn = pygame.Rect(405, 390, 190, 60)
hard_btn = pygame.Rect(620, 390, 190, 60)

start_btn = pygame.Rect(350, 490, 300, 65)

submit_btn = pygame.Rect(600, 340, 170, 60)
menu_btn = pygame.Rect(250, 470, 220, 60)
again_btn = pygame.Rect(530, 470, 220, 60)

input_rect = pygame.Rect(230, 340, 340, 60)

# Main loop
running = True

while running:

    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()

    draw_background()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                if state != MENU:
                    state = MENU
                else:
                    running = False

            if state == PLAYING:

                if event.key == pygame.K_RETURN:
                    check_guess()

                elif event.key == pygame.K_BACKSPACE:
                    guess_text = guess_text[:-1]

                elif event.unicode.isdigit() and len(guess_text) < 4:
                    guess_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if state == MENU:

                    if easy_btn.collidepoint(event.pos):
                        difficulty = "EASY"

                    elif medium_btn.collidepoint(event.pos):
                        difficulty = "MEDIUM"

                    elif hard_btn.collidepoint(event.pos):
                        difficulty = "HARD"

                    elif start_btn.collidepoint(event.pos):
                        start_game()

                elif state == PLAYING:

                    if submit_btn.collidepoint(event.pos):
                        check_guess()

                    elif input_rect.collidepoint(event.pos):
                        pass

                elif state == RESULT:

                    if again_btn.collidepoint(event.pos):
                        start_game()

                    elif menu_btn.collidepoint(event.pos):
                        state = MENU

    # MENU SCREEN
    if state == MENU:

        draw_text(
            "NUMBER", title_font, CYAN,
            WIDTH // 2, 110
        )

        draw_text(
            "MYSTERY", title_font, PURPLE,
            WIDTH // 2, 175
        )

        draw_text(
            "CAN YOU FIND THE SECRET NUMBER?",
            font, WHITE, WIDTH // 2, 245
        )

        draw_text(
            "SELECT DIFFICULTY",
            heading_font, WHITE, WIDTH // 2, 330
        )

        # Difficulty buttons
        for name, rect, color in [
            ("EASY", easy_btn, GREEN),
            ("MEDIUM", medium_btn, CYAN),
            ("HARD", hard_btn, PINK)
        ]:

            draw_button(name, rect, color, mouse_pos)

            if difficulty == name:
                pygame.draw.rect(
                    screen, WHITE,
                    rect.inflate(8, 8),
                    2, border_radius=16
                )

        draw_button(
            "START GAME", start_btn,
            PURPLE, mouse_pos
        )

        draw_text(
            "EASY: 1-50   |   MEDIUM: 1-100   |   HARD: 1-500",
            small_font, GRAY, WIDTH // 2, 590
        )

    # PLAYING SCREEN
    elif state == PLAYING:

        draw_text(
            "NUMBER MYSTERY",
            title_font, CYAN, WIDTH // 2, 65
        )

        # Main panel
        panel = pygame.Rect(130, 120, 740, 455)

        pygame.draw.rect(
            screen, PANEL, panel,
            border_radius=25
        )

        pygame.draw.rect(
            screen, PURPLE, panel,
            2, border_radius=25
        )

        low, high, _ = difficulties[difficulty]

        draw_text(
            f"DIFFICULTY: {difficulty}",
            font, CYAN, WIDTH // 2, 165
        )

        draw_text(
            f"FIND THE NUMBER BETWEEN {low} AND {high}",
            font, WHITE, WIDTH // 2, 220
        )

        draw_text(
            f"ATTEMPTS: {attempts} / {max_attempts}",
            font, YELLOW if False else GREEN,
            WIDTH // 2, 275
        )

        # Input box
        pygame.draw.rect(
            screen, (12, 15, 40),
            input_rect, border_radius=12
        )

        pygame.draw.rect(
            screen, CYAN, input_rect,
            2, border_radius=12
        )

        display_guess = guess_text if guess_text else "Enter number..."

        draw_text(
            display_guess,
            font,
            WHITE if guess_text else GRAY,
            input_rect.centerx,
            input_rect.centery
        )

        draw_button(
            "GUESS", submit_btn, PURPLE, mouse_pos
        )

        draw_text(
            message, font, message_color,
            WIDTH // 2, 435
        )

        # Previous guesses
        if history:
            draw_text(
                "YOUR GUESSES: " + "   ".join(map(str, history[-6:])),
                small_font, GRAY, WIDTH // 2, 505
            )

        draw_text(
            "PRESS ENTER TO SUBMIT | ESC TO MENU",
            small_font, GRAY, WIDTH // 2, 550
        )

    # RESULT SCREEN
    elif state == RESULT:

        draw_text(
            "MYSTERY RESULT",
            title_font, CYAN, WIDTH // 2, 120
        )

        if secret_number in history:

            draw_text(
                "CONGRATULATIONS!",
                heading_font, GREEN,
                WIDTH // 2, 230
            )

            draw_text(
                result_message,
                font, WHITE, WIDTH // 2, 290
            )

            draw_text(
                f"SECRET NUMBER: {secret_number}",
                font, YELLOW, WIDTH // 2, 350
            )

            draw_text(
                f"YOUR SCORE: {score}",
                heading_font, CYAN, WIDTH // 2, 405
            )

        else:

            draw_text(
                "GAME OVER!",
                heading_font, RED,
                WIDTH // 2, 230
            )

            draw_text(
                result_message,
                font, WHITE, WIDTH // 2, 290
            )

            draw_text(
                f"THE SECRET NUMBER WAS {secret_number}",
                font, YELLOW, WIDTH // 2, 355
            )

            draw_text(
                "BETTER LUCK NEXT TIME!",
                font, CYAN, WIDTH // 2, 405
            )

        draw_button(
            "MAIN MENU", menu_btn,
            PURPLE, mouse_pos
        )

        draw_button(
            "PLAY AGAIN", again_btn,
            CYAN, mouse_pos
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
