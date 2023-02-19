from pygame_vkeyboard import *

# Initializes your window object or surface your want
# vkeyboard to be displayed on top of.
surface = 800

def consumer(text):
    print('Current text : %s' % text)

# Initializes and activates vkeyboard
layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
keyboard = VKeyboard(surface, consumer, layout)