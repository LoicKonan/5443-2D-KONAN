import random
from pygame import Vector2
from objects.gameObject import GameObject
from utils.assets_manager import assetsManager

# This class represents a platform, which is made up of several game objects
class Platform:
    def __init__(self, pos, rows, cols):
        
        # Get the image of a single cell
        img = assetsManager.get("cell")

        # Get the size of a single cell
        tileSize = img.get_width()

        # Save the number of rows and columns in the platform
        self.rows = rows
        self.cols = cols
        self.pos = pos

        # Initialize an empty list to store the game objects that make up the platform
        self.gameObjects = []

        # Create game objects for each cell in the platform
        x = pos.x
        y = pos.y

        for row in range(rows):
            for col in range(cols):
                # Create a game object with the image of a single cell and add it to the list
                obj = GameObject(Vector2(x, y), img,"wall")
                self.gameObjects.append(obj)
                x += tileSize
                
            # Move to the next row
            x = pos.x
            y += tileSize

# This class generates a random map
class MapGenerator:
    def __init__(self):
        
        # Initialize empty lists to store the game objects and platforms in the map
        self.gameObjects = []
        self.platforms = []

        # Generate a random of Map number between 0 and 2
        Map = random.randrange(0,1)

        if Map == 0:
            self.platforms.append(Platform(Vector2(50,550),20,100) )
            self.platforms.append(Platform(Vector2(1050, 550), 20, 100))
            
            
        elif Map == 1:
            self.platforms.append(Platform(Vector2(50, 550), 2, 350))
            self.platforms.append(Platform(Vector2(50, 430), 2, 350))    

        # Add the game objects of each platform to the list of game objects in the map
        for platform in self.platforms:
            self.gameObjects += platform.gameObjects
