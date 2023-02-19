# Making all the words in words.py to upper case and print it to a file call lists.py 
import words
import random
import string
import os

# create a list of words
word_list = words.WORDS

# create a list of upper case words
upper_list = []

# loop through the list of words and make them upper case
for word in word_list:
    upper_list.append(word.upper())
    
# print the list of upper case words to a file
with open('lists.py', 'w') as f:
    f.write('WORDS = ')
    f.write(str(upper_list))
    f.close()
    
# print the list of upper case words to the console
print(upper_list)