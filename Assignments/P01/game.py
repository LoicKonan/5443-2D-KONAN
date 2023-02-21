import pygame
import random
import words
import itertools

# initialize pygame
pygame.init()

# screen setup colors
WHITE      = (255, 255, 255)
BLACK      = (0  ,   0,   0)
GREEN      = (0  , 255,   0)
YELLOW     = (255, 255,   0)
GRAY       = (128, 128, 128)
RED        = (255,   0,   0)
Blueviolet = (176,196,222)

# screen setup size constants
WIDTH  = 600
HEIGHT = 800

# This is the font.
huge_font   = pygame.font.Font("assets/FreeSansBold.otf", 56)
letter_font = pygame.font.Font("assets/FreeSansBold.otf", 50)
small_font  = pygame.font.Font("assets/FreeSansBold.otf", 25)


#
class WordleGame:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board  = [[" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " "]]
        
        self.turn              = 0
        self.letters           = 0
        self.KEY_WIDTH         = 40
        self.KEY_HEIGHT        = 40
        self.KEY_MARGIN        = 10
        self.box_width         = 65
        self.box_height        = 65
        self.green_box_height  = 80
        self.dist_Left         = 100
        self.dist_Top          = 120
        
        
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
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                self.handle_events(event)

            pygame.display.flip()
            
     
     
    # This Function will display a Title Wordle one letter at a time
    # It will also display the wordle in the middle of the screen
    def draw_title(self):
        title = huge_font.render("WORDLE", True, GREEN)
        self.screen.blit(title, (WIDTH / 2 - 125, 10))
        
        
    # This function will display the instruction on the screen
    # consist of 3 rectangle, one green, one yellow and one red.
    # if the rectangle is GREEN it means that the letter is part of the word and in the right column,
    # if the rectangle is YELLOW it means the letter is part of the word but not in the right column,
    # if the rectangle is RED the letter are not part of the word.
    def Instruction(self):
        pygame.draw.rect(self.screen, GREEN,  [90, 635, 25, 25], 0, 6)
        pygame.draw.rect(self.screen, YELLOW, [90, 685, 25, 25], 0, 6)
        pygame.draw.rect(self.screen, RED,    [90, 730, 25, 25], 0, 6)
        Instruction_text = small_font.render("Correct Letter / right spot", True, WHITE)
        self.screen.blit(Instruction_text, (130, 630))
        Instruction_text = small_font.render("Correct Letter / not in the right spot", True, WHITE)
        self.screen.blit(Instruction_text, (130, 680))
        Instruction_text = small_font.render("Wrong Letter", True, WHITE)
        self.screen.blit(Instruction_text, (130, 725))
    
    
    # This function will draw the letter entered by the player in GRAY
    # It will also draw the rectangle in which the player enter the letters in WHITE
    # It will also highlight the whole 5 letters word enter by the user in green to show the turn he is on.
    def draw_shape(self):
        for i, j in itertools.product(range(5), range(6)):
            pygame.draw.rect(self.screen, WHITE, [i * 80 + self.dist_Left, j * 80 + self.dist_Top, self.box_width, self.box_height], 2, 5)
            Letters_text = letter_font.render(self.board[j][i], True, GRAY)
            self.screen.blit(Letters_text, (i * 80 + (self.dist_Left + 15), j * 80 + self.dist_Top))
        pygame.draw.rect(self.screen, GREEN, [(self.dist_Left - 17), self.turn * 80 + (self.dist_Top - 8), WIDTH - 180, self.green_box_height], 4, 10)
    
    
    
    # This function call def check_words(self): will check if guess is correct, add game over conditions
    # it will also check if each letter entered is contain in the word. if the letter is part of the word
    # and in the right column it will draw the rectangle green, if the letter is part of the word
    # but not in the right column it will draw the rectangle yellow, if the letter are not part of the word
    # it will draw the rectangle red.
    def check_words(self):

        for i, j in itertools.product(range(5), range(6)):
            if self.secret_word[i] == self.board[j][i] and self.turn > j:
                pygame.draw.rect(self.screen, GREEN, [i * 80 + 100, j * 80 + self.dist_Top, self.box_height, self.box_width], 0, 6)
                # pygame.draw.rect(self.screen, GREEN, [i * 80 + 100, self.turn * 80 + 180, 65, 65], 0, 5)


            elif self.board[j][i] in self.secret_word and self.turn > j:
                pygame.draw.rect(self.screen, YELLOW, [i * 80 + 100, j * 80 + self.dist_Top, self.box_height, self.box_width], 0, 6)
            #   pygame.draw.rect(self.screen, YELLOW, [i * 80 + 100, self.turn * 80 + 180, 65, 65], 0, 5)

            # When the letter is not part of the word.  The letter will stay RED.
            elif self.board[j][i] != self.secret_word[i] and self.turn > j:
                pygame.draw.rect(self.screen, RED, [i * 80 + 100, j * 80 + self.dist_Top, self.box_height, self.box_width], 0, 6)     


        # check if guess is correct, add game over conditions
        for row in range(6):
            guess = self.board[row][0] + self.board[row][1] + self.board[row][2] + self.board[row][3] + self.board[row][4]
            if guess == self.secret_word and row < 6: 
                self.game_over = True
                self.draw_win()
                
        if self.turn == 6:
            self.game_over   = True
            self.turn_active = False
      

    
    def draw_board(self):
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
        self.screen.fill(BLACK)             # CALL THIS FUNCTION TO CLEAR THE SCREEN.

        # Good Job message
        win_text = huge_font.render("Good Job!!!", True, GREEN)
        self.screen.blit(win_text, [WIDTH / 2 - 150, HEIGHT - 700])
        # Display the secret word
        secret_text = huge_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])
        # Play again message.
        again_text = small_font.render("Press Enter or Space to play again", True, GREEN)
        self.screen.blit(again_text, [WIDTH / 2 - 200, HEIGHT - 250])
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
        secret_text = huge_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])
        # instructions to play again.
        text = small_font.render("Press Enter or Space to play again", True, RED)
        self.screen.blit(text, [WIDTH / 2 - 200, HEIGHT - 250])
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
    
    