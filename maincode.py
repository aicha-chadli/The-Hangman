import pygame
import random
import os


#setup pygame
# pygame.init()
# screen = pygame.display.set_mode((800 , 600))
# clock = pygame.time.Clock()
# running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
  screen.fill("lightgreen")
  pygame.display.flip()
  clock.tick(60)

pygame.quit()     

#read the words in mots.txt file
def load_word():
  with open("mots.txt","r") as file:
    return [line.strip() for line in file.readlines()]
  
#add a word to the file 
def add_word():
  new_word = input("add a new word to the list: ").strip().lower()
  with open("mots.txt", "a") as file:
       file.write(new_word + "\n")
  print("new word was added to the list !")
  
#choose a word randomly
def choose_random_word(words):
    return random.choice(words)
    
  
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Guess the Word - Hangman")
    FONT_SIZE = 40
    font = pygame.font.Font(None, FONT_SIZE)
    
    words = load_word()
    word_to_guess = choose_random_word(words)
    guessed_letters = set()
    errors = 0
    max_errors = 6
    
    clock = pygame.time.Clock()
    running = True 
    
    
    
    
  