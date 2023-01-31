import pygame
import random

# Initialize the game
pygame.init()

# Set window size and title
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Hangman Game")

# Load images for different parts of the stick figure
images = [pygame.image.load('part0.png'), pygame.image.load('part1.png'), pygame.image.load('part2.png'),
          pygame.image.load('part3.png'), pygame.image.load('part4.png'), pygame.image.load('part5.png'),
          pygame.image.load('part6.png')]

# List of words to choose from
word_list = ['python', 'java', 'javascript', 'ruby', 'go', 'c++']
word = random.choice(word_list)

# Set initial values for variables
word_to_guess = ["_" for i in word]
incorrect_guesses = 0
guessed_letters = []

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check if a letter was pressed on the keyboard
        if event.type == pygame.KEYDOWN:
            letter = chr(event.unicode).lower()

            # Check if the letter has not been guessed before
            if letter not in guessed_letters:
                guessed_letters.append(letter)

                # Check if the letter is in the word
                if letter in word:
                    for i in range(len(word)):
                        if word[i] == letter:
                            word_to_guess[i] = letter

                # Increase the number of incorrect guesses if the letter is not in the word
                else:
                    incorrect_guesses += 1

    # Clear the window
    win.fill((255, 255, 255))

    # Draw the stick figure
    win.blit(images[incorrect_guesses], (50, 50))

    # Draw the word to guess
    font = pygame.font.Font(None, 32)
    text = font.render(" ".join(word_to_guess), 1, (0, 0, 0))
    win.blit(text, (250, 250))

    # Update the display
    pygame.display.update()

    # Check if the player has won or lost
    if "_" not in word_to_guess:
        print("You won!")
        run = False
    elif incorrect_guesses == 6:
        print("You lost.")
        run = False

# Quit the game
pygame.quit()
