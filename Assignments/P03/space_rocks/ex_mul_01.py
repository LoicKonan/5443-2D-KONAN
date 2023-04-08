"""
This example has a series of classes to help with the multiplayer issue:

Messenger:
    Handles messaging for the players
BasicPlayer:
    Handles basic drawing and moving and is extended by `Player`
Player:
    Adds messaging to a basic player.
GameManager:
    Since we want most updating to be done locally, the game manager creates basic
    instances of each player (BasicPlayer) to move them around the screen. This reduces
    messaging to a minimum.
Globals:
    This was kind of an experiment to see about class level variables. I didn't want pygame
    to get instantiated until I grabbed to window location. So this was my solution.

This multiplayer example moves a bunch of dots around the screen. However, they are pygame
shapes and NOT sprites. I discovered sprites act much differently when moving via vectors.
So, I will create yet another version using sprites instead of shapes and attempt to get the
movement correct.

USAGE:

    python ex_99.py queue=game-01 player=player-02 windowLocation=400,400 color=Red

    - queue             : the exchange or channel you want to join
    - player            : the name or id of a player
    - windowLocation    : allows me to test better by moving pygame windows to different locations
    - color             : player dot color
"""


import pygame
from random import randint
import json
import sys
from rich import print
from threading import Thread
import math
import os
from pygame.math import Vector2

import pygame.display


# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

# bunches of named colors!
with open("colors.json") as f:
    colors = json.load(f)


class Messenger:
    """
    - Handles messaging (sending and receiving) for each player.
    - Requires a callback to be passed in so received messages can be handled.
    """

    def __init__(self, creds, callback=None):
        self.creds = creds
        self.callBack = callback

        if not self.creds:
            print(
                "Error: Message handler needs `creds` or credentials to log into rabbitmq. "
            )
            sys.exit()

        if not self.callBack:
            print(
                "Error: Message handler needs a `callBack` function to handle responses from rabbitmq. "
            )
            sys.exit()

        # Identify the user
        self.user = self.creds["user"]

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)

    def send(self, **kwargs):
        """Sends the message to a target or broadcasts to all."""
        target = kwargs.get("target", "broadcast")
        self.commsSender.threadedSend(
            target=target, sender=self.user, body=json.dumps(kwargs), debug=False
        )


class BasicPlayer:
    """
    - Handles basic updating and movement for a "dot" (player)
    - Doesn't require anything. But at minimum name should probably match a valid rabbitmq name.
    """

    def __init__(self, **kwargs):
        """_summary_

        Args:
            color (tuple)           : rgb value (r,g,b)
            id (string)             : unique identifier for player
            location (tuple)        : (x,y)
            screen (pygame surface) : pygame surface to display player
        """
        # init sprite base class
        super(BasicPlayer, self).__init__()

        # get player basics from kwargs
        self.screen = kwargs.get("screen", None)  # copy of screen to display dot on
        self.name = kwargs.get("name", None)  # players name or id
        self.location = kwargs.get("location", (randint(25, 400), randint(25, 400)))

        # convert tuple to a vector
        self.location = pygame.math.Vector2(self.location)

        self.speed = 1
        self.ticks = 0
        self.width, self.height = self.screen.get_size()
        self.lastUpdated = pygame.time.get_ticks()
        self.velocity = pygame.math.Vector2()
        self.direction = (1, 1)
        self.target = (0, 0)

    def move(self, keys=None):
        """
        - Change player position based on velocity.
        - Stop player if space bar is pressed.
        """
        # print(f"updating {self.color}")
        if keys:
            if keys[pygame.K_SPACE]:
                self.velocity.x = 0
                self.velocity.y = 0

        # Move the sprite towards the target each frame
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y

        # Wrap player around the screen so
        # they never get lost.
        if self.location.x > self.width:
            self.location.x = 0
        if self.location.x < 0:
            self.location.x = self.width
        if self.location.y > self.height:
            self.location.y = 0
        if self.location.y < 0:
            self.location.y = self.height

    def goto(self, target_x, target_y):
        """Starts player moving towards the x,y coords passed
        in from a mouse click event.
        """
        # distance not used, but could be if we had AI players you wanted to move
        # toward another player.
        distance = math.sqrt(
            (target_x - self.location.x) ** 2 + (target_y - self.location.y) ** 2
        )

        # set players direction based on clicked location and current dot location
        self.direction = (
            target_x - self.location.x,
            target_y - self.location.y,
        )

        # Normalize the direction vector to get a unit vector
        direction_normalized = pygame.math.Vector2(self.direction).normalize()

        # Calculate the velocity vector by multiplying the direction vector by the speed
        self.velocity = direction_normalized * self.speed

    def setSpeed(self, speed):
        """This gets called when any numeric key is pressed from 0-9"""
        self.speed = speed
        direction_normalized = pygame.math.Vector2(self.direction).normalize()

        # change velocity based on input speed
        self.velocity = direction_normalized * self.speed

    def update(self, keys=None):
        """Updates position and calls draw for player"""
        self.move(keys)
        self.draw()

    def draw(self):
        """Draws the dot. Could be more complex for an animated sprite or
        similar, but one line is good for now.
        """
        # draw the dot
        pygame.draw.circle(self.screen, self.color, self.location, 10)


class Player(BasicPlayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.creds = kwargs.get("creds", None)
        self.callback = kwargs.get("callback", None)
        self.id = self.creds["user"]
        self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 50

    def timeToBroadCast(self):
        """check to see if there was enough delay to broadcast again"""
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def goto(self, target_x, target_y):
        print("child goto")
        self.target = (target_x, target_y)
        super(Player, self).goto(target_x, target_y)
        print("broadcasting target")
        self.broadcastData(
            {
                "target": self.target,
                "location": (self.location.x, self.location.y),
                "speed": self.speed,
                "color": self.color,
            }
        )

    def setSpeed(self, speed):
        """Yup. This sets the players speed.
            It also broadcasts the speed to everyone else.
        Args:
            speed (int) : players speed
        """
        super(Player, self).setSpeed(speed)
        print("broadcasting speed")
        self.broadcastData(
            {
                "target": self.target,
                "location": (self.location.x, self.location.y),
                "speed": self.speed,
                "color": self.color,
            }
        )



############################################################
# GLOBALS
############################################################
class Globals:
    """A class mainly for one reason, placing game window in new xy location"""

    winx = 0
    winy = 0
    winsize = (400, 400)
    screen = None
    clock = None
    fps = 60

    def __new__(cls, x, y):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (int(x), int(y))
        pygame.init()
        cls.screen = pygame.display.set_mode(cls.winsize)
        cls.clock = pygame.time.Clock()
        instance = super().__new__(cls)
        return instance


def main(creds, x, y, color=None):
    globals = Globals(x, y)
    manager = GameManager(globals.screen)

    localPlayer = Player(
        screen=globals.screen, creds=creds, callback=manager.callBack, color=color
    )

    manager.addPlayer(player=localPlayer, localPlayer=True)
    # set the window title
    pygame.display.set_caption(f"{creds['user']}")

    # create list for lookup for keys 0-9
    # The keys 0-9 are ascii 48-57
    # run the game loop
    running = True
    while running:
        # clear the screen
        globals.screen.fill((255, 255, 255))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    localPlayer.update(keys)

            elif event.type == pygame.MOUSEBUTTONUP:
                # Get the position of the mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)
                localPlayer.goto(mouse_x, mouse_y)

        # move the dot based on key input
        keys = pygame.key.get_pressed()
        localPlayer.update(keys)

        manager.update()

        # update the screen
        pygame.display.flip()

        globals.clock.tick(globals.fps)

    # quit Pygame
    pygame.quit()





def usage():
    print("Need: queue and player ")
    print(
        "Example: python ex_99.py queue=game-01 player=player-01 windowLocation=100,100 color=blue"
    )
    sys.exit()


if __name__ == "__main__":
    """
    Example: python ex_99.py queue=game-01 player=player-01 windowLocation=100,100 color=blue
    """
    args, kwargs = mykwargs(sys.argv)

    queue = kwargs.get("queue", None)
    player = kwargs.get("player", None)
    windowLocation = kwargs.get("windowLocation", (100, 100))
    color = kwargs.get("color", "Red")

    color = colors[color]["rgb"]

    print(windowLocation)

    if not isinstance(windowLocation, tuple):
        windowLocation = tuple(windowLocation.split(","))

    x, y = windowLocation

    # if None in [queue, player]:
    #     usage()

    # player credentials built based on which temp player chosen (player-01 through player-25)
    creds = {
        "exchange": queue,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": player + "2023!!!!!",
    }

    main(creds, x, y, color)
