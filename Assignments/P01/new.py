import pygame
import random
import pygame.mixer
import words
import itertools


pygame.init()
pygame.mixer.init()

# screen setup Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY   = (128, 128, 128)
RED    = (255, 0, 0)

# screen setup size constants
WIDTH  = 600
HEIGHT = 800

# This is the font.
huge_font   = pygame.font.Font("assets/FreeSansBold.otf", 56)
letter_font = pygame.font.Font("assets/FreeSansBold.otf", 50)
small_font  = pygame.font.Font("assets/FreeSansBold.otf", 30)

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
        self.turn         = 0
        self.letters      = 0
        self.turn_active  = True
        # self.secret_word  = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
        self.game_over    = False
        self.KEY_WIDTH    = 40
        self.KEY_HEIGHT   = 40
        self.KEY_MARGIN   = 10
        self.clock        = pygame.time.Clock()
        
        self.secret_word = "ETHER"
        self.angle = 0
        self.rotate_speed = 1
        # self.win_sound  = pygame.mixer.Sound("assets/win.ogg")
        # self.lose_sound = pygame.mixer.Sound("assets/lost.mp3")

        pygame.display.set_caption("Wordle Game")
        self.icon = pygame.image.load("assets/Icon.png")
        pygame.display.set_icon(self.icon)

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill(BLACK)
            self.check_words()
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
        title = huge_font.render("WORDLE", True, YELLOW)
        self.screen.blit(title, (WIDTH / 2 - 125, 50))
    
    
    # This function will draw the letter entered by the player in GRAY
    # It will also draw the rectangle in which the player enter the letters in WHITE
    # It will also highlight the whole 5 letters word enter by the user in green to show the turn he is on.
    def draw_shape(self):
        box_width, box_height, green_box_height = 65, 65, 80
        dist_Left, dist_Top   = 100, 180
        for i, j in itertools.product(range(5), range(6)):
            pygame.draw.rect(self.screen, WHITE, [i * 80 + dist_Left, j * 80 + dist_Top, box_width, box_height], 2, 5)
            text = letter_font.render(self.board[j][i], True, GRAY)
            self.screen.blit(text, (i * 80 + (dist_Left + 10), j * 80 + dist_Top))
        pygame.draw.rect(self.screen, GREEN, [(dist_Left - 17), self.turn * 80 + (dist_Top - 8), WIDTH - 180, green_box_height], 4, 10)
    
    
    
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
        
        
    def check_words(self):
        if self.turn == 6:
            self.game_over   = True
            self.turn_active = False
            
            # if self.secret_word in self.board:
            #     # self.win_sound.play()
            # else:
            #     # self.lose_sound.play()
                
                
    def draw_board(self):
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_title()
            self.draw_shape()
            # self.draw_keyboard()
            
    def draw_game_over(self):
        if self.secret_word in self.board:
            self.draw_win()
        else:
            self.draw_lose()
            
            
            
    def draw_win(self):
        win_text = huge_font.render("Good shit!!!", True, GREEN)
        self.screen.blit(win_text, [WIDTH / 2 - 125, HEIGHT / 2 - 50])
        again_text = small_font.render("Press Space to play again", True, GREEN)
        self.screen.blit(again_text, [WIDTH / 2 - 125, HEIGHT / 2 + 50])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        return
                    pygame.display.flip()
                    
                    
                    
                    
    def draw_lose(self):
        # Display the secret word
        secret_text = huge_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])
        
        # instructions to play again.
        text = small_font.render("Press Space to play again", True, RED)
        self.screen.blit(text, [WIDTH / 2 - 180, HEIGHT - 250])
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        return
                    pygame.display.flip()
                    
                    
    
    # def draw_keyboard(self):
    #     pass
                
                
if __name__ == "__main__":
    game = WordleGame()
    game.run()
    
    