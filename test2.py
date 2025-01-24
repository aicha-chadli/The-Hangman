import pygame
import random
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 40

# Load words from the file
def load_words(file_name="mots.txt"):
    try:
        with open(file_name, "r") as file:
            words = [line.strip().upper() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        sys.exit()

# Choose a random word from the list
def choose_random_word(words):
    return random.choice(words)

def draw_hangman(screen, errors):
    # Define the new X offset for the hangman and gallows
    offset_x = 500  # Shift everything to the right
    base_y = 450    # Base height for the gallows and hangman

    # Draw gallows
    pygame.draw.line(screen, WHITE, (offset_x - 100, base_y), (offset_x + 100, base_y), 5)  # Base
    pygame.draw.line(screen, WHITE, (offset_x, base_y), (offset_x, base_y - 300), 5)       # Pole
    pygame.draw.line(screen, WHITE, (offset_x, base_y - 300), (offset_x + 100, base_y - 300), 5)  # Top beam
    pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 300), (offset_x + 100, base_y - 250), 5)  # Rope

    # Draw the hangman parts based on the number of errors
    if errors >= 1:  # Head
        pygame.draw.circle(screen, WHITE, (offset_x + 100, base_y - 230), 20, 2)
    if errors >= 2:  # Body
        pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 210), (offset_x + 100, base_y - 140), 2)
    if errors >= 3:  # Left arm
        pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 190), (offset_x + 80, base_y - 160), 2)
    if errors >= 4:  # Right arm
        pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 190), (offset_x + 120, base_y - 160), 2)
    if errors >= 5:  # Left leg
        pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 140), (offset_x + 80, base_y - 90), 2)
    if errors >= 6:  # Right leg
        pygame.draw.line(screen, WHITE, (offset_x + 100, base_y - 140), (offset_x + 120, base_y - 90), 2)


# Display the word with blanks
def display_word(screen, font, word, guessed_letters):
    display_text = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    text_surface = font.render(display_text, True, WHITE)
    screen.blit(text_surface, (50, 500))

# Display guessed letters
def display_guessed_letters(screen, font, guessed_letters):
    text_surface = font.render(f"try to guess the word: {', '.join(sorted(guessed_letters))}", True, WHITE)
    screen.blit(text_surface, (50, 550))

# Main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Guess the Word - Hangman")
    font = pygame.font.Font(None, FONT_SIZE)

    words = load_words()
    word = choose_random_word(words)
    guessed_letters = set()
    errors = 0
    max_errors = 6

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                letter = event.unicode.upper()
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter not in word:
                        errors += 1

        # Check for win/loss
        if errors >= max_errors:
            display_text = font.render(f"You lost! The word was {word}.", True, RED)
            screen.blit(display_text, (50, 300))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        if all(letter in guessed_letters for letter in word):
            display_text = font.render("Congratulations! You guessed the word!", True, GREEN)
            screen.blit(display_text, (50, 300))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        # Draw the hangman and update the display
        draw_hangman(screen, errors)
        display_word(screen, font, word, guessed_letters)
        display_guessed_letters(screen, font, guessed_letters)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()

