
# from time import sleep
# import pygame
# import pygame_menu
# from pygame_menu import themes
 
# pygame.init()
# surface = pygame.display.set_mode((600, 400))
 
# def set_difficulty(value, difficulty):
#     print(value)
#     print(difficulty)
 
# def start_the_game():
#     mainmenu._open(loading)
#     pygame.time.set_timer(update_loading, 30)
 
# def level_menu():
#     mainmenu._open(level)
 
 
# mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_SOLARIZED)
# mainmenu.add.text_input('Name: ', default='username')
# mainmenu.add.button('Play', start_the_game)
# mainmenu.add.button('Levels', level_menu)
# mainmenu.add.button('Quit', pygame_menu.events.EXIT)
 
# level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
# level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
 
# loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
# loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
# arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
# update_loading = pygame.USEREVENT + 0
 
# while True:
#     events = pygame.event.get()
#     for event in events:
#         if event.type == update_loading:
#             progress = loading.get_widget("1")
#             progress.set_value(progress.get_value() + 1)
#             if progress.get_value() == 100:
#                 pygame.time.set_timer(update_loading, 0)
#         if event.type == pygame.QUIT:
#             exit()
 
#     if mainmenu.is_enabled():
#         mainmenu.update(events)
#         mainmenu.draw(surface)
#         if (mainmenu.get_current().get_selected_widget()):
#             arrow.draw(surface, mainmenu.get_current().get_selected_widget())
 
#     pygame.display.update()


from pygame import *
import pygame 
import math
import random as rand
from abc import ABC, abstractmethod 

#display & music settings
pygame.init()
logo = pygame.image.load("assets/hangman6.png")
pygame.display.set_icon(logo)
music = pygame.mixer.music.load("assets/AWM.mp3")
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound("assets/click.wav")
width = 800
height = 500
display = pygame.display.set_mode((width, height))
background = (255,255,255)
base_font = pygame.font.SysFont("comicsans",32)
tittle_font = pygame.font.SysFont("dejavuserif",40)
clock = pygame.time.Clock()
pygame.display.set_caption("Hangman")

#button
radius = 20
gap = 15
alphabet = []
startx = 550
starty = 50
for i in range(26):
    if i<24:
        x = startx + gap * 2 + ((radius * 2 + gap) * (i % 4))#590, 592,2, 594,4, 596,6, 598,8, 601
        y = starty + ((i // 4) * (gap + radius * 2))# 50, 50, 50, 50, 120, 120, 120, 120, 190, 190, 190, 190
    else:
        x = startx + gap * 2 + ((radius * 2 + gap) * ((i+1) % 4))
        y = starty + (((i+1) // 4) * (gap + radius * 2))
    alphabet.append([x, y, chr(65 + i), True])

#images
images=[]
DEFAULT_IMAGE_SIZE = (250,253)
for i in range(7):
    image = pygame.image.load(f"assets/hangman{str(i)}.png")
    image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
    images.append(image)

#assets
list_text=(['CHICKEN','CAT','BEAR','BIRD','TIGER','RABBIT','ZEBRA'],['APPLE','BANANA','POTATO','MEAT','ORANGE','CHOCOLATE','CAKE'],['YOUTUBER','PROGRAMMER','POLICE','DOCTOR','PILOT','CHEF','DRIVER'])
stats = 0
answered=[]

#parent class
class Hangman(ABC):
    global quest
    def __init__(self,name):
        self.name = name

    def close():
        pygame.quit()

    def out_display(self,word):
        self.word = word
        pygame.time.delay(1000)
        display.fill(background)
        win_image = pygame.image.load("assets/winman.png")
        win_image = pygame.transform.scale(win_image, DEFAULT_IMAGE_SIZE)
        if self.word == "You Won":
            display.blit(win_image, (280,50))
        text = base_font.render(word, 1, (0,0,0))
        display.blit(text, (width/2 - text.get_width()/2, (height/2 - text.get_height()/2)+30))
        text_out = base_font.render(f"Answer : {quest}", 1, (0,0,0))
        display.blit(text_out, (width/2 - text_out.get_width()/2, (height/2 - text_out.get_height()/2)+60))
        pygame.display.update()
        pygame.time.delay(3000)
        Hangman.close()

    def show():
        display.fill(background)

        #draw title
        text = base_font.render("Hangman Game", 1, (0,0,0))
        display.blit(text, (width/2 - text.get_width()/2, 20))

        #draw topic
        topic = base_font.render(f"Topic : {tpc}", 1, (0,0,0))
        display.blit(topic, (width/2 - topic.get_width()/2, 50))
        
        #draw words
        show_alphabet = ""
        for check in quest:
            if check in answered:
                show_alphabet += check + " "
            else:
                show_alphabet += "_ "
        text = base_font.render(show_alphabet, 1, (0,0,0))
        display.blit(text, (200, 400))

        #draw buttons
        for check in alphabet:
            x, y, txt, status = check
            if status:
                pygame.draw.circle(display, (0,0,0), (x, y), radius,3)
                text = base_font.render(txt, 1, (0,0,0))
                display.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
        
        #draw images    
        display.blit(images[stats], (150,100))
        pygame.display.update()

    #main program
    @abstractmethod
    def main_p(self):
        global stats
        global alphabet
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Hangman.close()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    click.play()
                    for check in alphabet:
                        x, y, txt, status = check
                        if status:
                            cek = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
                            if cek <= radius:
                                check[3] = False
                                answered.append(txt)
                                print(answered)
                                if txt not in quest:
                                    stats += 1
            Hangman.show()

            game = True
            for check in quest:
                if check not in answered:
                    game = False
                    break
            
            if game:
                Hangman.out_display(self,"You Won")
                break
            if stats == 6:
                Hangman.out_display(self,"You Lost")
                break

class Animal(Hangman):
    quest = rand.choice(list_text[0])
    def __init__(self,name):
        super().__init__(name)
    
    def out_display(self,word):
        super().out_display(word)
    
    def show():
        super().show()

    def main_p(self):
        super().main_p()

class Food(Hangman):
    quest = rand.choice(list_text[1])
    def __init__(self,name):
        super().__init__(name)

    def out_display(self,word):
        super().out_display(word)
    
    def show():
        super().show()

    def main_p(self):
        super().main_p()

class Jobs(Hangman):
    quest = rand.choice(list_text[2])
    def __init__(self,name):
        super().__init__(name)

    def out_display(self,word):
        super().out_display(word)
    
    def show():
        super().show()

    def main_p(self):
        super().main_p()
        
def Intro():
    display.fill(background)
    intro_check = True
    xvar=400
    yvar=250
    xclue = 600
    yclue = 350
    cot=0
    while intro_check:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Hangman.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                click.play()
                cot+=1
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                cek_clue = math.sqrt((xclue - xpos)**2 + (yclue - ypos)**2)
                if cek_clue <= radius+27:
                    Clue()
                    intro_check = False
                elif cek <= radius+40:
                    intro_check = False
                if cot > 6:
                    cot=0
                    display.fill(background)
            pygame.display.update()

            text = tittle_font.render("Welcome to Hangman Game", 1, (0,0,0))
            display.blit(text, (width/2 - text.get_width()/2, 20))

            text = base_font.render("START", 1, (0,0,0))
            display.blit(text, (width/2 - text.get_width()/2, yvar-20))
            
            pygame.draw.circle(display, (0,0,0), (xvar,yvar), radius+40,6)
            display.blit(images[cot], (150,100))

            clue = base_font.render("Clue", 1, (0,0,0))
            display.blit(clue, (xclue-27, yclue-20))

            pygame.draw.circle(display, (0,0,0), (xclue,yclue), radius+30,6)

        pygame.display.update()

def Clue():
    display.fill(background)
    clue_image=pygame.image.load("assets/clue.png")
    clue_check = True
    xvar=50
    yvar=425
    while clue_check:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Hangman.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                click.play()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= radius+40:
                    clue_check = False
                    Intro()
                    return False
            Clue = tittle_font.render("Clue List", 1, (0,0,0))
            display.blit(Clue, (width/2 - Clue.get_width()/2, 20))

            Back = base_font.render("Back", 1, (0,0,0))
            display.blit(Back, (xvar, yvar))

            display.blit(clue_image, (100,100))
            pygame.display.update()

        pygame.display.update()

Intro()
pygame.time.delay(500)
quest_rand=rand.randint(0,2)
quest = rand.choice(list_text[quest_rand])
if quest_rand == 0:
    tpc = "Animal"
elif quest_rand == 1:
    tpc = "Food"
elif quest_rand == 2:
    tpc = "Jobs"
play = "Player 1 "
player=Food(play)
player.main_p()

pygame.quit()