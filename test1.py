import pygame
import random
import os

# Charger les mots depuis le fichier
def load_words():
    with open("mots.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

# Ajouter un mot au fichier
def add_word():
    new_word = input("Entrez un nouveau mot : ").strip().lower()
    with open("mots.txt", "a") as file:
        file.write(new_word + "\n")
    print("Mot ajouté avec succès !")

# Choisir un mot aléatoire
def choose_random_word(words):
    return random.choice(words)

# Initialiser Pygame
def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((900,520))
    pygame.display.set_caption("Jeu du Pendu")
    fond = pygame.image.load("Guessing-game.webp").convert()
    screen.blit(fond, (0,0))
    return screen

# Dessiner le pendu
def draw_hangman(screen, errors):
    # Dessiner les éléments du pendu en fonction du nombre d'erreurs
    if errors >= 1:
        pygame.draw.circle(screen, (255, 0, 0), (400, 150), 50, 5)  # Tête
    if errors >= 2:
        pygame.draw.line(screen, (255, 0, 0), (400, 200), (400, 350), 5)  # Corps
    if errors >= 3:
        pygame.draw.line(screen, (255, 0, 0), (400, 250), (350, 300), 5)  # Bras gauche
    if errors >= 4:
        pygame.draw.line(screen, (255, 0, 0), (400, 250), (450, 300), 5)  # Bras droit
    if errors >= 5:
        pygame.draw.line(screen, (255, 0, 0), (400, 350), (350, 450), 5)  # Jambe gauche
    if errors >= 6:
        pygame.draw.line(screen, (255, 0, 0), (400, 350), (450, 450), 5)  # Jambe droite

# Jeu principal
def main():
    words = load_words()
    word_to_guess = choose_random_word(words)
    guessed = ["_"] * len(word_to_guess)
    used_letters = set()
    errors = 0
    max_errors = 6

    screen = initialize_pygame()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fond = pygame.image.load("Guessing-game.webp").convert()
    
    running = True
    while running:
        screen.blit(fond, (0,0))

        # Afficher le mot à deviner
        word_display = " ".join(guessed)
        text = font.render(word_display, True, (0, 0, 0))
        screen.blit(text, (100, 100)) 

        # Afficher les lettres utilisées
        used_letters_display = "Lettres utilisées : " + ", ".join(sorted(used_letters))
        text = font.render(used_letters_display, True, (0, 0, 0))
        screen.blit(text, (100, 150))

        # Dessiner le pendu
        draw_hangman(screen, errors)

        # Vérifier les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                letter = event.unicode.lower()
                if letter.isalpha() and letter not in used_letters:
                    used_letters.add(letter)
                    if letter in word_to_guess:
                        for i, char in enumerate(word_to_guess):
                            if char == letter:
                                guessed[i] = letter
                    else:
                        errors += 1

        # Vérifier les conditions de victoire ou défaite
        if "_" not in guessed:
            print("Félicitations, vous avez gagné !")
            running = False
        elif errors >= max_errors:
            print(f"Vous avez perdu ! Le mot était : {word_to_guess}")
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Menu principal
def menu():
    while True:
        print("\n--- Jeu du Pendu ---")
        print("1. Jouer")
        print("2. Ajouter un mot")
        print("3. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            main()
        elif choice == "2":
            add_word()
        elif choice == "3":
            print("À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

# Démarrer le programme
if __name__ == "__main__":
    menu()
