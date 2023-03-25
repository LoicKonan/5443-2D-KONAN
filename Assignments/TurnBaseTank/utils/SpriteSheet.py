import pygame

from utils.util import utils


# This is a SpriteSheet class that loads an image and divides it into frames.
# This allows for playing an animation, setting the animation parameters, and flipping the frames.
class SpriteSheet: # check santa.png

    def __init__(self, texture, rows, cols):
        
        # Initialize SpriteSheet object with default values
        self.countTime = 0 # Count time for changing frames
        self.ffrom = 0     # First frame index to play
        self.fto = 0       # Last frame index to play
        self.current = 0   # Current frame index
        self.time = 0      # Time to change frames
        self.loop = False  # Flag to indicate if sprite should loop

        # Load texture and calculate number of rows and columns
        self.texture = texture
        self.rows = rows
        self.cols = cols

        # Create a list to store the frames, Divide texture into frames
        self.sheet = texture
        self.frames = []
        
        # Get width and height of sprite sheet
        self.width = self.sheet.get_rect().width
        self.height = self.sheet.get_rect().height

        # Calculate size of each row and column in sprite sheet
        sizeRow = self.sheet.get_rect().height / rows
        sizeCol = self.sheet.get_rect().width / cols
        
        # Extract each frame of sprite sheet and store them in frames list
        for row in range(rows):
            for col in range(cols):
                img = self.image_at((col * sizeCol, row * sizeRow, sizeCol, sizeRow),(0,0,0)).convert_alpha()
                self.frames.append(img)

    # Method to extract image from sprite sheet based on a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Method to play sprite animation
    def play(self):
        # Play animation frame by frame
        self.countTime += utils.deltaTime()

        # If time to change frame is reached, change frame index
        if self.countTime >= self.time:
            self.countTime = 0
            self.current += 1

            # If last frame is reached and loop flag is true, start over
            if self.current > self.fto:
                self.current = self.ffrom if self.loop else self.fto

    
    # Method to set which frames to play and the time to change them
    def setPlay(self, ffrom, fto, time, loop): # play sheet from to
        self.ffrom = ffrom
        self.fto = fto
        self.time = time
        self.loop = loop
        self.current = ffrom

    # Method to get the current frame of the sprite
    def getCurrentFrame(self):
        return self.frames[self.current]

    # Method to flip the sprite horizontally
    def flip(self,flipX): 
        # Flip the frames horizontally
        self.frames = []
        
        # Calculate size of each row and column in sprite sheet
        sizeRow = self.sheet.get_rect().height / self.rows
        sizeCol = self.sheet.get_rect().width / self.cols
        
        # The for loop iterates over each row and column in the sprite sheet, 
        # creating a new image from the specified rectangle and flipping it horizontally if specified. 
        # The resulting image is added to the list of frames for the sprite sheet.
        for row in range(self.rows):
            for col in range(self.cols):
                img = self.image_at((col * sizeCol, row * sizeRow, sizeCol, sizeRow), (0, 0, 0)).convert_alpha()
                img = pygame.transform.flip(img, flipX, False)
                self.frames.append(img)
