import pygame
from pygame import Vector2
pygame.font.init()
import time

from objects.Explosion import Explosion
from objects.Missile import Missile
from objects.Projectile import Projectile
from objects.Tank import Tank
from utils.map_generator import MapGenerator
from utils.sounds import Sounds, sounds
from utils.util import utils


class Game:
    def __init__(self):
        # Initialize all variables and game objects
        self.map = None
        self.winner = None
        self.currentTurn = None
        self.tank1 = None
        self.tank2 = None
        self.currentLevel = 0
        self.gameObjects = []
        self.velocity = 0.20
        self.currentProjectile = None

        # Start a new game
        self.newGame()


    def newGame(self):
        # Reset variables and game objects for a new game
        self.currentTurn = -1
        self.winner = None
        self.gameObjects = []
        self.map = MapGenerator()
        self.tank1 = Tank(Vector2(200, 100))
        self.tank2 = Tank(Vector2(1070, 100))
        
        # Add game objects to the list
        self.gameObjects += self.map.gameObjects
        self.gameObjects.append(self.tank1)
        self.gameObjects.append(self.tank2)

        # utils.camera.follow(None)

    def update(self):
        # Update the camera position
        # utils.camera.update()
        
        

        # Rotate the cannon of the current tank based on whose turn it is
        if self.currentTurn == -1:
            self.tank1.rotateCannon()
        else:
            self.tank2.rotateCannon()

        # Check if a tank has gone out of bounds
        if self.tank1.pos.y > 720:
            self.winner = 1
            return
        
        if self.tank2.pos.y > 720:
            self.winner = -1
            return

        # Update all game objects and apply gravity to tanks and projectiles
        for object in self.gameObjects:
            object.update()

            # gravity
            if object.type in ["tank", "Projectile1", "Projectile2"]:
                object.applyForce(Vector2(0, self.velocity))  

            # Check for collisions between tanks and walls
            if object.type == "tank":
                self.checkTankWithWall(object)

            # Check for collisions between projectiles and walls
            if object.type in ["Projectile1", "Projectile2"]:
                self.checkProjectileCollision(object)
                
                # Remove the projectile and add an explosion effect if it collides with a wall
                if object.destroy:
                    self.gameObjects.remove(object)
                    # utils.camera.follow(None)
                    self.gameObjects.append(Explosion(Vector2(object.pos.x - 32,object.pos.y - 32)))
                    sounds.play("explosion")

                    # Change the turn if the projectile was a Projectile or a Missile
                    if isinstance(object, (Projectile, Missile)):
                        self.currentTurn *= -1
                    break

            # Check for collisions between Projectile1 and Tank2        
            if object.type == "Projectile1" and utils.collide(object,self.tank2) and self.tank2 is not None:
                self.winner = -1
                
                if self.gameObjects.__contains__(self.tank2):
                    self.gameObjects.remove(self.tank2)
                self.gameObjects.append(Explosion(self.tank2.pos))
                sounds.play("explosion")
                return

            # Check for collisions between Projectile2 and Tank1
            if object.type == "Projectile2" and utils.collide(object,self.tank1) and self.tank1 is not None:
                self.winner = 1
                
                if self.gameObjects.__contains__(self.tank1):
                    self.gameObjects.remove(self.tank1)
                self.gameObjects.append(Explosion(self.tank1.pos))
                sounds.play("explosion")
                return

            # removes walls that are marked to be destroyed from the gameObjects list
            if object.destroy and object.type == "wall":
                self.gameObjects.remove(object)

    # This method checks for collision between a tank and a wall
    def checkTankWithWall(self, tank):
        
        # iterate through all game objects and check for collision and object type
        for otherObj in self.gameObjects:
            if utils.collide(tank, otherObj) and otherObj.type == "wall":
                # call onWallCollide method on wall object
                otherObj.onWallCollide(tank)

    # This method checks for collision between a projectile and a wall
    def checkProjectileCollision(self,projectile):
        
        # iterate through all game objects and check for collision and object type
        for otherObj in self.gameObjects:
            if utils.collide(projectile, otherObj) and otherObj.type == "wall":
                # set destroy flag to true for both objects
                otherObj.destroy = True
                projectile.destroy = True
                
        # if projectile is destroyed
        if projectile.destroy:
            
            # iterate through all game objects and check for collision and object type
            for otherObj in self.gameObjects:
                if otherObj.type == "wall" and utils.distance(projectile.pos.x,projectile.pos.y,otherObj.pos.x,otherObj.pos.y) < 50:
                    # set destroy flag to true for wall object
                    otherObj.destroy = True


    # This method handles keyboard key press events
    def onKeyDown(self, key):
        # if there is a winner
        if self.winner is not None:
            # if space key is pressed, start new game
            if key == pygame.K_SPACE:
                self.newGame()
            return

        # if w key is pressed and there is a current projectile
        if key == pygame.K_w and self.currentProjectile is not None:
            # get two projectiles from current projectile
            p1, p2 = self.currentProjectile.getProjectiles()
           
            # add both projectiles to game objects
            self.gameObjects.append(p1)
            self.gameObjects.append(p2)
            
            # set current projectile to None and play sound
            self.currentProjectile = None
            sounds.play("split")

        # if camera has a target, return
        # if utils.camera.target is not None:
        #     return
        
        # if it's player 1's turn call onKeyDown method on tank1 object
        if self.currentTurn == -1:
            self.tank1.onKeyDown(key)
            
        # else if it's player 2's turn call onKeyDown method on tank2 object
        else:
            self.tank2.onKeyDown(key)

        # if q key is pressed, decrease velocity
        if key == pygame.K_q:
            self.velocity -= 0.1
            self.velocity = max(self.velocity, 0.1)
            
        # if e key is pressed, increase velocity
        elif key == pygame.K_e:
            self.velocity += 0.1
            self.velocity = min(self.velocity, 1)


    # This method handles keyboard key release events
    def onKeyUp(self, key):
        # if there is a winner, return
        if self.winner is not None:
            return

        # if it's player 1's turn, call onKeyUp method on tank1 object
        if self.currentTurn == -1:
            self.tank1.onKeyUp(key)
            
        # if it's player 2's turn, call onKeyUp method on tank2 object
        else:
            self.tank2.onKeyUp(key)


    # # This method handles mouse button down events
    def onMouseDown(self, event):
        
        # if there is a winner, return
        if self.winner is not None:
            return

        # If the camera is following an object, also return
        # if utils.camera.target is not None:
        #     return
        
        # If it's player 1's turn, call the onMouseDown function for tank1
        if self.currentTurn == -1:
            self.tank1.onMouseDown(event)
            
        # If it's player 2's turn, call the onMouseDown function for tank2
        else:
            self.tank2.onMouseDown(event)
    
        

        # This function is called when a mouse button is released
    def onMouseUp(self, event):
        # If there is already a winner, the game is over, so return
        if self.winner is not None:
            return
        # If the camera is following an object, also return
        # if utils.camera.target is not None:
        #     return

        # If it's player 1's turn, call the onMouseUp function for tank1
        if self.currentTurn == -1:
            
            self.tank1.onMouseUp(event)
            # Get the projectile from tank1
            projectile = self.tank1.getProjectile()
            # Set the type of the projectile to "Projectile1"
            projectile.type = "Projectile1"
            # Add the projectile to the list of game objects
            self.gameObjects.append(projectile)
            # Make the camera follow the projectile
            # utils.camera.follow(projectile)

            # If the projectile is a Projectile, set it as the current projectile
            if isinstance(projectile, Projectile):
                self.currentProjectile = projectile
            # If it's a Missile, set the target to tank2
            elif isinstance(projectile, Missile):
                projectile.setTarget(self.tank2)
        else:
            
            self.tank2.onMouseUp(event)
            # Get the projectile from tank2
            projectile = self.tank2.getProjectile()
            # Set the type of the projectile to "Projectile2"
            projectile.type = "Projectile2"
            # Add the projectile to the list of game objects
            self.gameObjects.append(projectile)
            
            # Make the camera follow the projectile
            # utils.camera.follow(projectile)

            # If the projectile is a Projectile, set it as the current projectile
            if isinstance(projectile, Projectile):
                self.currentProjectile = projectile
            # If it's a Missile, set the target to tank1
            elif isinstance(projectile, Missile):
                projectile.setTarget(self.tank1)

        # Play the sound for firing the projectile
        sounds.play("projectile")



    # This function is called to draw the game
    def draw(self):
        
        # Draw game instructions and Title.
        utils.drawText(Vector2(400, 20), "Tank Battle Game", (244, 244, 244), 48)
        utils.drawText(Vector2(525, 100), "Move: A/D", (244, 244, 244), 24)
        utils.drawText(Vector2(525, 130), "Shoot: Mouse", (244, 244, 244), 24)
        utils.drawText(Vector2(525, 160), "Special: W", (244, 244, 244), 24)
        utils.drawText(Vector2(480, 190), "Gravity: Q/E + : " + "{:.2f}".format(self.velocity), (244, 244, 244), 24)

       
        # Draw Team USA top left Corner and Top Right Corner Team RUSSIA
        utils.drawText(Vector2(110, 40), "Team USA", (100, 200, 219), 24)
        utils.drawText(Vector2(1040, 40), "Team Russia", (231, 76, 60), 24) 
        
        
        # Show who Turn it is if game is not over
        if self.winner is None:
            if self.currentTurn == -1:
                utils.drawText(Vector2(115, 190), "USA Turn",  (100, 200, 219), 24)
            else:
                utils.drawText(Vector2(1045, 190), "Russia Turn", (231, 76, 60), 24) 
        
        
        # Iterates through each game object in the gameObjects list
        for obj in self.gameObjects:
            # Draws the object on the screen at its position, taking into account the position of the camera
            utils.screen.blit(obj.img, (obj.pos.x - utils.camera.pos.x, obj.pos.y - utils.camera.pos.y))
            
            # Calls the draw method of the object
            obj.draw()


        # If the game has been won by player 1, display a "Player 1 win!" message
        if self.winner == -1:
            utils.screen.fill((0, 0, 0))  # Clear the screen with black color
            utils.drawText(Vector2(500, 100), "Player 1 win!!!", (244, 23, 23), 43) 
            
            # Add USA Flag
            usa_flag = pygame.image.load("assets/usa.jpg").convert_alpha()
            usa_flag = pygame.transform.scale(usa_flag, (300, 180))
            utils.screen.blit(usa_flag, (500, 200))
            utils.drawText(Vector2(465, 440), "Press 'space' to restart!", (166, 23, 23), 32)
        
        # If the game has been won by player 2, display a "Player 2 win!" message
        elif self.winner == 1:
            utils.screen.fill((0, 0, 0))  # Clear the screen with black color
            utils.drawText(Vector2(500, 100), "Player 2 win!!!", (244, 23, 23), 43)
           
            # Add Russia Flag
            russia_flag = pygame.image.load("assets/russia.png").convert_alpha()
            russia_flag = pygame.transform.scale(russia_flag, (300, 180))
            utils.screen.blit(russia_flag, (500, 200))
            utils.drawText(Vector2(465, 440), "Press 'space' to restart!", (166, 23, 23), 32)