import pygame
from pygame.locals import *

import os 
import random
from string import ascii_letters

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Hangman")

class Hangman():
  def __init__(self):
    self.word_file_path = r"C:\Users\hp\Desktop\The-Hangman\words.txt"
    self._initialize_game()
    self.background_color = (155, 120, 70)
    self.gallow_color = (0, 0, 0)
    self.body_color = (255, 253, 175)
    self.font = pygame.font.SysFont("Courier New", 20)
    self.FPS = pygame.time.Clock()

  def _initialize_game(self):
    self._load_secret_word()
    self.wrong_guesses = []
    self.wrong_guess_count = 0
    self.taking_guess = True

  def _load_secret_word(self):
    with open(self.word_file_path, "r") as file:
      words = file.read().split("\n")
      self.secret_word = random.choice(words)
      self.guessed_word = "-" * len(self.secret_word)

  def _gallow(self):
    pygame.draw.rect(screen, self.gallow_color, pygame.Rect(75, 280, 120, 10))
    pygame.draw.rect(screen, self.gallow_color, pygame.Rect(128, 40, 10, 240))
    pygame.draw.rect(screen, self.gallow_color, pygame.Rect(128, 40, 80, 10))
    pygame.draw.rect(screen, self.gallow_color, pygame.Rect(205, 40, 10, 30))

  def _man_pieces(self):
    if self.wrong_guess_count > 0:
      pygame.draw.circle(screen, self.body_color, [210, 85], 20, 0)
    if self.wrong_guess_count > 1:
      pygame.draw.rect(screen, self.body_color, pygame.Rect(206, 105, 8, 45))
    if self.wrong_guess_count > 2:
      pygame.draw.line(screen, self.body_color, [183, 149], [200, 107], 6)
    if self.wrong_guess_count > 3:
      pygame.draw.line(screen, self.body_color, [231, 149], [218, 107], 6)
    if self.wrong_guess_count > 4:
      pygame.draw.line(screen, self.body_color, [189, 198], [208, 148], 6)
    if self.wrong_guess_count > 5:
      pygame.draw.line(screen, self.body_color, [224, 198], [210, 148], 6)

  def _guess_taker(self, guess_letter):
    if guess_letter in ascii_letters:
      if guess_letter in self.secret_word and guess_letter not in self.guessed_word:
        self._right_guess(guess_letter)
      elif guess_letter not in self.secret_word and guess_letter not in self.wrong_guesses:
        self._wrong_guess(guess_letter)

  def _right_guess(self, guess_letter):
    index_positions = [index for index, item in enumerate(self.secret_word) if item == guess_letter]
    for i in index_positions:
      self.guessed_word = self.guessed_word[:i] + guess_letter + self.guessed_word[i+1:]
    screen.fill(pygame.Color(self.background_color), (10, 370, 390, 20))

  def _wrong_guess(self, guess_letter):
    self.wrong_guesses.append(guess_letter)
    self.wrong_guess_count += 1
    self._man_pieces()

  def _message(self):
    if self.guessed_word == self.secret_word:
      self.taking_guess = False
      screen.fill(pygame.Color(0,0,79), (40, 218, 320, 30))
      message = self.font.render("YOU WIN!!", True, (255,235,0))
      screen.blit(message,(152,224))
      pygame.display.flip()
      pygame.time.delay(2000)  # Wait for 2 seconds
      self._menu()

    elif self.wrong_guess_count == 6:
      self.taking_guess = False
      screen.fill(pygame.Color("grey"), (40, 218, 320, 30))
      message = self.font.render("GAME OVER YOU LOSE!!", True, (150,0,10))
      screen.blit(message,(78,224))
      word = self.font.render(f"secret word: {self.secret_word}", True, (255,255,255))
      screen.blit(word,(10,300))
      pygame.display.flip()
      pygame.time.delay(2000)  # Wait for 2 seconds
      self._menu()

  def _menu(self):
    screen.fill(self.background_color)
    menu_texts = ["1. Play", "2. Add a Word", "3. Quit"]
    for i, text in enumerate(menu_texts):
      menu_item = self.font.render(text, True, (255,255,255))
      screen.blit(menu_item, (120, 150 + i * 40))
    pygame.display.flip()
    choice = None
    while choice not in ['1', '2', '3']:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        elif event.type == pygame.KEYDOWN:
          choice = event.unicode
    if choice == '1':
      self._initialize_game()
      self.main()
    elif choice == '2':
      self._add_word()
    elif choice == '3':
      pygame.quit()
      exit()

  def _add_word(self):
    new_word = input("Enter a new word: ").strip().lower()
    if new_word.isalpha():
      with open(self.word_file_path, "a") as file:
        file.write(f"\n{new_word}")
      print("Word added successfully!")
    self._menu()

  def main(self):
    screen.fill(self.background_color)
    self._gallow()
    instructions = self.font.render('Press any key to take Guess', True, (9,255,78))
    screen.blit(instructions,(35,460))
    running = True
    while running:
      guessed_word = self.font.render(f"guessed word: {self.guessed_word}", True, (0,0,138))
      screen.blit(guessed_word,(10,370))
      wrong_guesses = self.font.render(f"wrong guesses: {' '.join(self.wrong_guesses)}", True, (125,0,0))
      screen.blit(wrong_guesses,(10,420))
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if self.taking_guess:
            self._guess_taker(event.unicode)
      self._message()
      pygame.display.flip()
      self.FPS.tick(60)
    pygame.quit()

if __name__ == "__main__":
  h = Hangman()
  h._menu()
