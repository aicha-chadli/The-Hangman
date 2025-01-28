import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)

# Load words from file
def load_words(filename):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words

# Select a random word
def get_random_word(words):
    return random.choice(words)

# Draw the hangman
def draw_hangman(screen, attempts):
    if attempts < 1:
        return
    # Base
    pygame.draw.line(screen, BLACK, (100, 500), (300, 500), 5)
    # Pole
    pygame.draw.line(screen, BLACK, (200, 500), (200, 100), 5)
    # Top bar
    pygame.draw.line(screen, BLACK, (200, 100), (400, 100), 5)
    # Rope
    pygame.draw.line(screen, BLACK, (400, 100), (400, 150), 5)
    if attempts < 2:
        return
    # Head
    pygame.draw.circle(screen, BLACK, (400, 180), 30, 5)
    if attempts < 3:
        return
    # Body
    pygame.draw.line(screen, BLACK, (400, 210), (400, 350), 5)
    if attempts < 4:
        return
    # Left arm
    pygame.draw.line(screen, BLACK, (400, 250), (350, 300), 5)
    if attempts < 5:
        return
    # Right arm
    pygame.draw.line(screen, BLACK, (400, 250), (450, 300), 5)
    if attempts < 6:
        return
    # Left leg
    pygame.draw.line(screen, BLACK, (400, 350), (350, 400), 5)
    if attempts < 7:
        return
    # Right leg
    pygame.draw.line(screen, BLACK, (400, 350), (450, 400), 5)

# Main game loop
def main():
    words = load_words("mots.txt")
    word = get_random_word(words).upper()
    guessed = ["_"] * len(word)
    attempts = 0
    max_attempts = 7
    guessed_letters = []

    running = True
    while running:
        screen.fill(WHITE)

        # Draw hangman
        draw_hangman(screen, attempts)

        # Display word
        display_word = " ".join(guessed)
        word_text = FONT.render(display_word, True, BLACK)
        screen.blit(word_text, (100, 50))

        # Display guessed letters
        guessed_text = SMALL_FONT.render(f"Guessed: {', '.join(guessed_letters)}", True, BLACK)
        screen.blit(guessed_text, (100, 520))

        # Check for win or lose
        if "_" not in guessed:
            win_text = FONT.render("You Win!", True, RED)
            screen.blit(win_text, (500, 300))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        elif attempts >= max_attempts:
            lose_text = FONT.render(f"You Lose! The word was: {word}", True, RED)
            screen.blit(lose_text, (500, 300))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key).upper()
                    if letter not in guessed_letters:
                        guessed_letters.append(letter)
                        if letter in word:
                            for i, char in enumerate(word):
                                if char == letter:
                                    guessed[i] = letter
                        else:
                            attempts += 1

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
