##############################################################################################
#  
#      Author:           Loic Konan
#      Email:            loickonan.lk@gmail.com
#      Label:            Wordle Game
#      Title:            Program 1
#      Course:           CMPS 5443 
#      Semester:         Spring 2023
#      Description:
#                        This is a Wordle game in pygame.
#                        Wordle is a guessing game in which players try to 
#                        guess a secret word by making multiple attempts.
#                        The game features 5 word, and players have 
#                        6 chances to guess it correctly. After each guess, the game provides 
#                        feedback in the form of colored squares.
#                        The colored squares indicate which letters in the guess match the 
#                        secret word and are in the correct position.
#                        Players can use this feedback to eliminate incorrect letters
#                        and narrow down their subsequent guesses. The game ends when the 
#                        player guesses the word correctly or runs out of attempts.
#  
#
#      Usage:
#                        python game.py          - driver program
#
#      Files:            game.py, words1.py, assets/Icon.png, assets/FreeSansBold.otf
#
#      Date:             02/21/2023
#
#  
##############################################################################################
import pygame 
import random 
import words1   
import itertools 

# initialize pygame
pygame.init()

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


##############################################################################################
# class WordleGame:
#
#   - This is the main class of the game
#   - It will display the title, the instruction, the wordle, the letter entered by the player
#   - It will also check if the word entered by the player is correct or not.
#   - It will also check if the player has won or lost the game.
#
##############################################################################################
class WordleGame:
    
    
    ########################################################################################
    #     def __init__(self):
    #
    #         - Constructor
    #         - Initializes the game screen with the dimensions WIDTH and HEIGHT.
    #         - Initializes 2-D list with 6 rows and 5 columns filled with empty spaces.
    #         - Sets the initial values for game variables.
    #         - Loads and sets the game window's caption and icon.
    #
    ########################################################################################
    
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
        self.box_width         = 60
        self.box_height        = 60
        self.green_box_height  = 73
        self.dist_Left         = 130
        self.dist_Top          = 90

        self.game_over    = False
        self.turn_active  = True
        self.clock        = pygame.time.Clock()

        pygame.display.set_caption("Wordle Game")
        self.icon = pygame.image.load("assets/Icon.png")
        pygame.display.set_icon(self.icon)
        
        # self.secret_word  = words1.WORDS1[random.randint(0, len(words1.WORDS1) - 1)]
        self.secret_word = "ETHER"



    ########################################################################################
    # def run(self):
    #
    #   - This method is the main game loop, which runs as long as the game is active.
    #   - Uses the pygame clock object to regulate the frame rate to 60 frames per second.
    #   - Fills the screen with the color black to clear the previous frame.
    #   - Calls other methods that draw various game elements on the screen.
    #   - Handles user events, such as keyboard input, updates the game state accordingly.
    #   - Flips the display to show the updated frame on the screen.
    #
    ########################################################################################

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill(BLACK)
            self.check_words1()
            self.draw_title()
            self.draw_shape()
            self.Instruction()
            self.result()
            self.score()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                self.handle_events(event)

            pygame.display.flip()
            
     
     
    ##########################################################
    # def draw_title(self):
    #
    #   - This method will display Wordle as a Title.
    #
    ##########################################################
    
    def draw_title(self):
        title = letter_font.render("WORDLE", True, GREEN)
        self.screen.blit(title, (WIDTH / 2 - 110, HEIGHT - 625))
        
        
        
    ###################################################################################
    # def Instruction(self):
    #
    #   - This method will display the instruction on the screen
    #   - 3 rectangle, Green, Yellow and Red.
    #   - GREEN means the letter is part of the word and in the right position,
    #   - YELLOW means the letter is part of the word but not in the right position,
    #   - RED means the letter are not part of the word.
    #
    ####################################################################################

    def Instruction(self):
        
        # Draw the different rectangles.
        pygame.draw.rect(self.screen, GREEN,  [WIDTH - 560, HEIGHT - 150, self.box_width - 30, self.box_height - 30], 5, 4)
        pygame.draw.rect(self.screen, YELLOW, [WIDTH - 560, HEIGHT - 100, self.box_width - 30, self.box_height - 30], 5, 4)
        pygame.draw.rect(self.screen, RED,    [WIDTH - 560, HEIGHT - 50,  self.box_width - 30, self.box_height - 30], 5, 4)
        
        # Display the instruction text
        Instruction_text = small_font.render("Correct Letter / right spot", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 148))
        Instruction_text = small_font.render("Correct Letter / not in the right spot", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 100))
        Instruction_text = small_font.render("Wrong Letter", True, WHITE)
        self.screen.blit(Instruction_text, (WIDTH - 520, HEIGHT - 48))
    
    
    
    ########################################################################################
    # def draw_shape(self):
    #
    #   - This method will draw the letter entered by the player in GRAY
    #   - It will draw the rectangle in which the player enter the letters in WHITE
    #   - It will draw a Green rectangle to show what row you on.
    #
    ########################################################################################

    def draw_shape(self):
        for i, j in itertools.product(range(5), range(6)):
            # The rectangle that will contain the letter.
            pygame.draw.rect(self.screen, WHITE, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 3, 8)
            
            # The letter that will be entered by the player.
            Letters_text = letter_font.render(self.board[j][i], True, GRAY)
            self.screen.blit(Letters_text, (i * 65 + (self.dist_Left + 10), j * 65 + self.dist_Top - 21))
            
        # Draw the rectangle that show what row you on.
        pygame.draw.rect(self.screen, GREEN, [(self.dist_Left - 6), self.turn * 65 + (self.dist_Top - 25), WIDTH - 275, self.green_box_height - 10], 3, 10)
    

    
    ##############################################################################
    # def check_words1(self):
    #
    #   - This method will check the entered word by the user.
    #   - It will compare the entered word with the secret word and
    #   - set the appropriate values for the green, yellow and red color boxes.
    #
    ##############################################################################
    
    def check_words1(self):
        for i, j in itertools.product(range(5), range(6)):
            # When the letter is part of the word and in the right position. The square will turn GREEN.
            if self.secret_word[i] == self.board[j][i] and self.turn > j:
                pygame.draw.rect(self.screen, GREEN, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)
                
            # When the letter is part of the word but not in the right position. The square will turn YELLOW.
            elif self.board[j][i] in self.secret_word and self.turn > j:
                pygame.draw.rect(self.screen, YELLOW, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)

            # When the letter is not part of the word.  The letter will stay RED.
            elif self.board[j][i] != self.secret_word[i] and self.turn > j:
                pygame.draw.rect(self.screen, RED, [i * 65 + self.dist_Left, j * 65 + self.dist_Top - 20, self.box_width - 8, self.box_height - 8], 0, 8)

        # check if guess is correct, add game over conditions
        for row in range(6):
            guess = self.board[row][0] + self.board[row][1] + self.board[row][2] + self.board[row][3] + self.board[row][4]
            
            # If the guess is correct, then game over and go to the draw_win method.
            if guess == self.secret_word and row < 6: 
                self.game_over = True
                self.draw_win()
        
        # After the last guess it Game over, you can't type no more.    
        if self.turn == 6:
            self.game_over   = True
            self.turn_active = False


    ##############################################################################
    # def result(self):
    #   
    #   - Clear the screen 
    #   - Call the right method depending if the player won or lost the game.
    #
    #
    ##############################################################################

    def result(self):
        if self.game_over:
            self.screen.fill(BLACK)             
            if self.secret_word in self.board:
                self.draw_win()
            else:
                self.draw_lose()
       
       
    
    #########################################################################################
    # def handle_events(self, event):
    #   
    #   - Responsible for handling events such as keyboard inputs.
    #   - The handle_keydown method is called when the user presses a key on the keyboard 
    #   - The handle_textinput method is called when the user enters text input
    #
    #########################################################################################
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.TEXTINPUT and self.turn_active and not self.game_over:
            self.handle_textinput(event)



    ########################################################################
    # def handle_keydown(self, event):
    #   
    #   - The method handles different key press events in the game.
    #
    #########################################################################
    
    def handle_keydown(self, event):
        
        # If the user presses the backspace deletes the last typed letter from the board.
        if event.key == pygame.K_BACKSPACE and self.letters > 0:
            self.board[self.turn][self.letters - 1] = ' '
            self.letters -= 1
            
        # If Enter key and the game is not over, moves to the next turn and resets the letter count to 0.    
        elif event.key == pygame.K_RETURN and not self.game_over:
            self.turn += 1
            self.letters = 0
            
        # If Enter key and the game is over, the method resets the game.
        elif event.key == pygame.K_RETURN:
            self.reset_game()
            
        
        # You can only enter word with 5 letters.
        if self.letters == 5:
            self.turn_active = False
            
        # If you enter less than 5 letters, then you can enter a letter
        if self.letters < 5:
            self.turn_active = True



    ##################################################################################
    # def handle_textinput(self, event):
    #   
    #   - This handle text input events that occur when a player enters a letter.
    #
    ##################################################################################
    def handle_textinput(self, event):
        entry = event.__getattribute__('text')
        
        # if the user entered a letter, make it uppercase and assigns it to a position
        if entry != " ":
            entry = entry.upper()
            self.board[self.turn][self.letters] = entry
            self.letters += 1
            
            
            
 #########################################################
 # def draw_win(self):
 #
 #     - Tell them to Hit Enter or Space to play again
 #     - Show the correct word
 #     - Show the Good Job message
 #
 #########################################################
            
    def draw_win(self):
        
        # Calling these functions   
        self.screen.fill(BLACK)             
        self.score()
             
        # Good Job message
        win_text = letter_font.render("Good Job!!!", True, GREEN)
        self.screen.blit(win_text, (WIDTH / 2 - 160, HEIGHT - 180))
        
        # Display the secret word
        secret_text = letter_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])

        # Play again message.
        again_text = small_font.render("Press Enter or Space to play again", True, GREEN)
        self.screen.blit(again_text, [WIDTH / 2 - 180, HEIGHT - 250])
        pygame.display.flip()
        
        # This while loop listens for events until the user either closes the game or Hit SPACE/ENTER. 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        return
                    pygame.display.flip()
                    
                    
                    
########################################################
# def draw_lose(self):
#
#     - Tell them to Hit Enter or Space to play again
#     - Show the correct word
#     - Show the Game Over message
#
########################################################

    def draw_lose(self):

        # Calling these functions        
        self.score()
        
        # Display the secret word
        secret_text = letter_font.render(self.secret_word, True, WHITE)
        self.screen.blit(secret_text, [WIDTH / 2 - 90, HEIGHT - 500])

        # GAME OVER YOU LOSE!!!
        lose_text = small_font.render("GAME OVER ............. LOSER!!!", True, RED)
        self.screen.blit(lose_text, (WIDTH / 2 - 160, HEIGHT - 180))
        
        # instructions to play again.
        text = small_font.render("Press Enter or Space to play again", True, RED)
        self.screen.blit(text, [WIDTH / 2 - 180, HEIGHT - 250])
        pygame.display.flip()

        # This listens for events until the user either closes the game or presses SPACE/ENTER. 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        return
                    pygame.display.flip()
                    
  

##############################################################################################
# def timer_T(self):
#
#     - This method will show a 60 seconds clock to the player on the top left of the screen. 
#     - The clock will start counting down from 60 seconds when the game starts.
#     - The clock will stop counting down when the game is over.
#     - The clock will reset to 60 seconds when the player starts a new game.
#     - When the clock get to 0 seconds and the player wasn't able to guess the correct word the game 
#     - will go to the draw_lose function. 
#
#
##############################################################################################                  




##############################################################################################
# def score(self):
#
#     - This method will show the player's score on the top right of the screen.
#     - The score will start at 0 when the game starts.
#     - The score will increase by 10 point for every green box
#     - The score will increase by 5 point for every yellow box
#     - The score will reset to 0 when the player starts a new game.
#     - The player will see the score in the draw_win and draw_lose screen.
#
##############################################################################################   
  
    def score(self):
        score = 0
        for row, col in itertools.product(range(5), range(5)):
            if self.board[row][col] == self.secret_word[col]:
                score += 10
            elif self.board[row][col] in self.secret_word:
                score += 5
        score_text = small_font.render("Score: " + str(score), True, WHITE)
        self.screen.blit(score_text, [WIDTH - 110, 20])

        return score
        
  
##############################################################################################
# def reset_game(self):
#
#     - resets the game by reinitialize the game's data attributes to their initial values.
#     - clears the player's previous guesses by resetting the game board with blank spaces.
#     - resets the game-over status of the game to False.
#     - generates a new secret word for the player to guess. 
#
##############################################################################################

    def reset_game(self):
        self.turn        = 0
        self.letters     = 0
        self.game_over   = False
        self.secret_word = words1.WORDS1[random.randint(0, len(words1.WORDS1) - 1)]        
        self.board       = [  [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "]]
        
        self.turn_active = True
        self.game_over   = False            
 
 
                
#######################
#    Main Driver
#######################
if __name__ == "__main__":
    game = WordleGame()
    game.run()
    
    