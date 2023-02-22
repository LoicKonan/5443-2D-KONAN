##############################################################################################
#  
#      Author:           Loic Konan
#      Email:            loickonan.lk@gmail.com
#      Label:            Wordle
#      Title:            Program 1
#      Course:           CMPS 5443 
#      Semester:         Spring 2023
#      Description:
#                        This This is a Wordle game in pygame.
#                        Wordle is a guessing game in which players try to 
#                        guess a secret word by making multiple attempts.
#                        The game features a five-letter word, and players have 
#                        6 to guess it correctly. After each guess, the game provides 
#                        feedback in the form of colored squares.
#                        The colored squares indicate which letters in the guess match the 
#                        secret word and are in the correct position.
#                        Players can use this feedback to eliminate incorrect letters
#                        and narrow down their subsequent guesses. The game ends when the 
#                        player guesses the word correctly or runs out of attempts.
#  
#
#      Usage:
#                        python game.py          : driver program
#
#      Files:            game.py, words.py, assets/Icon.png, assets/FreeSansBold.otf
#
#      Date:             02/21/2023
#
#  
#  
##############################################################################################
import pygame
import random
import words
import itertools


pygame.init()
pygame.mixer.init()

# screen setup colors
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 255,   0)
YELLOW     = (255, 255,   0)
GRAY       = (128, 128, 128)
RED        = (255,   0,   0)

# screen setup size constants
WIDTH  = 600
HEIGHT = 630

# This is the font.
letter_font   = pygame.font.Font("assets/FreeSansBold.otf", 45)
small_font    = pygame.font.Font("assets/FreeSansBold.otf", 20)

class WordleGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board  = [[" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "]]
        
        self.turn              = 0
        self.letters           = 0
        self.box_width         = 60
        self.box_height        = 60
        self.green_box_height  = 73
        self.dist_Left         = 130
        self.dist_Top          = 90
        
        
        self.clock        = pygame.time.Clock()
        self.game_over    = False
        self.turn_active  = True
        # self.secret_word  = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
        self.secret_word = "ETHER"
        


        pygame.display.set_caption("Wordle Game")
        self.icon = pygame.image.load("assets/Icon.png")
        pygame.display.set_icon(self.icon)


    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill(BLACK)
            self.check_words()
            self.draw_title()
            self.draw_shape()
            self.Instruction()
            self.result()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                self.handle_events(event)

            pygame.display.flip()
            
     
     
    # This Function will display a Title Wordle one letter at a time
    # It will also display the wordle in the middle of the screen
    def draw_title(self):
        title = letter_font.render("WORDLE", True, GREEN)
        self.screen.blit(title, (WIDTH / 2 - 110, HEIGHT - 625))
        
        
    # This function will display the instruction on the screen
    # consist of 3 rectangle, one green, one yellow and one red.
    # if the rectangle is GREEN it means that the letter is part of the word and in the right column,
    # if the rectangle is YELLOW it means the letter is part of the word but not in the right column,
    # if the rectangle is RED the letter are not part of the word.
    def Instruction(self):
        pygame.draw.rect(self.screen, GREEN,  [WIDTH - 560, HEIGHT - 150, self.box_width - 30, self.box_height - 30], 5, 4)
        pygame.draw.rect(self.screen, YELLOW, [WIDTH - 560, HEIGHT - 100, self.box_width - 30, self.box_height - 30], 5, 4)
        pygame.draw.rect(self.screen, RED,    [WIDTH - 560, HEIGHT - 50,  self.box_width - 30, self.box_height - 30], 5, 4)
        Instruction_text = small_font.render("Correct Letter / right spot", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 148))
        Instruction_text = small_font.render("Correct Letter / not in the right spot", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 100))
        Instruction_text = small_font.render("Wrong Letter", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 48))
    
    
    # This function will draw the letter entered by the player in GRAY
    # It will also draw the rectangle in which the player enter the letters in WHITE
    # It will also highlight the whole 5 letters word enter by the user in green to show the turn he is on.
    def draw_shape(self):
        for i, j in itertools.product(range(5), range(6)):
            pygame.draw.rect(self.screen, WHITE, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 3, 8)
            Letters_text = letter_font.render(self.board[j][i], True, GRAY)
            self.screen.blit(Letters_text, (i * 65 + (self.dist_Left + 10), j * 65 + self.dist_Top - 21))
        pygame.draw.rect(self.screen, GREEN, [(self.dist_Left - 6), self.turn * 65 + (self.dist_Top - 25), WIDTH - 270, self.green_box_height - 10], 3, 10)
    
    
    
    # This function call def check_words(self): will check if guess is correct, add game over conditions
    # it will also check if each letter entered is contain in the word. if the letter is part of the word
    # and in the right column it will draw the rectangle green, if the letter is part of the word
    # but not in the right column it will draw the rectangle yellow, if the letter are not part of the word
    # it will draw the rectangle red.
    def check_words(self):

        for i, j in itertools.product(range(5), range(6)):
            if self.secret_word[i] == self.board[j][i] and self.turn > j:
                pygame.draw.rect(self.screen, GREEN, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)

            elif self.board[j][i] in self.secret_word and self.turn > j:
                pygame.draw.rect(self.screen, YELLOW, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)

            # When the letter is not part of the word.  The letter will stay RED.
            elif self.board[j][i] != self.secret_word[i] and self.turn > j:
                pygame.draw.rect(self.screen, RED, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)

        # check if guess is correct, add game over conditions
        for row in range(6):
            guess = self.board[row][0] + self.board[row][1] + self.board[row][2] + self.board[row][3] + self.board[row][4]
            if guess == self.secret_word and row < 6: 
                self.game_over = True
                self.draw_win()
                
        if self.turn == 6:
            self.game_over   = True
            self.turn_active = False

    
    def result(self):
        if self.game_over:
            self.screen.fill(BLACK)             # CALL THIS FUNCTION TO CLEAR THE SCREEN.
            if self.secret_word in self.board:
                self.draw_win()
            else:
                self.draw_lose()
       
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.TEXTINPUT and self.turn_active and not self.game_over:
            self.handle_textinput(event)


    def handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE and self.letters > 0:
            self.board[self.turn][self.letters - 1] = ' '
            self.letters -= 1
        elif event.key == pygame.K_RETURN and not self.game_over:
            self.turn += 1
            self.letters = 0
        elif event.key == pygame.K_RETURN:
            self.reset_game()

        if self.letters == 5:
            self.turn_active = False
        if self.letters < 5:
            self.turn_active = True


    def handle_textinput(self, event):
        entry = event.__getattribute__('text')
        if entry != " ":
            entry = entry.upper()
            self.board[self.turn][self.letters] = entry
            self.letters += 1
            
            
    def draw_win(self):
        self.screen.fill(BLACK)             
        
        # Good Job message
        win_text = letter_font.render("Good Job!!!", True, GREEN)
        self.screen.blit(win_text, [WIDTH / 2 - 150, HEIGHT - 10])
        
        # Display the secret word
        secret_text = letter_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])
        

        # Play again message.
        again_text = small_font.render("Press Enter or Space to play again", True, GREEN)
        self.screen.blit(again_text, [WIDTH / 2 - 180, HEIGHT - 250])
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        return
                    pygame.display.flip()
                    
                    
                    
    def draw_lose(self):
        # Display the secret word
        secret_text = letter_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])

        # instructions to play again.
        text = small_font.render("Press Enter or Space to play again", True, RED)
        self.screen.blit(text, [WIDTH / 2 - 180, HEIGHT - 250])
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        return
                    pygame.display.flip()
  

    def reset_game(self):
        self.turn        = 0
        self.letters     = 0
        self.game_over   = False
        self.secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]        
        self.board       = [  [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "]]
        
        self.turn_active = True
        self.game_over   = False            
 
                
if __name__ == "__main__":
    game = WordleGame()
    game.run()
    
    