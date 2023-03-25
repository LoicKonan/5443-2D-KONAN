import pygame
from pygame import Vector2

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
        self.velocity = 0.58
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

        utils.camera.follow(None)

    def update(self):
        # Update the camera position
        utils.camera.update()

        # Rotate the cannon of the current tank based on whose turn it is
        if self.currentTurn == -1:
            self.tank1.rotateCannon()
        else:
            self.tank2.rotateCannon()

        # Check if a tank has gone out of bounds
        if self.tank1.pos.y > 2000:
            self.winner = 1
            return
        
        if self.tank2.pos.y > 2000:
            self.winner = -1
            return

        # Update all game objects and apply gravity to tanks and projectiles
        for object in self.gameObjects:
            object.update()

            if object.type in ["tank", "Projectile1", "Projectile2"]:
                object.applyForce(Vector2(0, self.velocity))  # gravity

            # Check for collisions between tanks and walls
            if object.type == "tank":
                self.checkTankWithWall(object)

            # Check for collisions between projectiles and walls
            if object.type in ["Projectile1", "Projectile2"]:
                self.checkProjectileCollision(object)
                
                # Remove the projectile and add an explosion effect if it collides with a wall
                if object.destroy:
                    self.gameObjects.remove(object)
                    utils.camera.follow(None)
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
            p1, p2 = self.currentProjectile.getProjectiles()
            self.gameObjects.append(p1)
            self.gameObjects.append(p2)
            self.currentProjectile = None
            sounds.play("split")

        if utils.camera.target is not None:
            return
        if self.currentTurn == -1:
            self.tank1.onKeyDown(key)
        else:
            self.tank2.onKeyDown(key)

        if key == pygame.K_q:
            self.velocity -= 0.1
            self.velocity = max(self.velocity, 0.1)
        elif key == pygame.K_e:
            self.velocity += 0.1
            self.velocity = min(self.velocity, 1)


    def onKeyUp(self, key):
        if self.winner is not None:
            return

        if self.currentTurn == -1:
            self.tank1.onKeyUp(key)
        else:
            self.tank2.onKeyUp(key)

    def onMouseDown(self, event):
        if self.winner is not None:
            return

        if utils.camera.target is not None:
            return
        if self.currentTurn == -1:
            self.tank1.onMouseDown(event)
        else:
            self.tank2.onMouseDown(event)

    def onMouseUp(self, event):
        if self.winner is not None:
            return
        if utils.camera.target is not None:
            return

        if self.currentTurn == -1:
            self.tank1.onMouseUp(event)
            projectile = self.tank1.getProjectile()
            projectile.type = "Projectile1"
            self.gameObjects.append(projectile)
            utils.camera.follow(projectile)

            if isinstance(projectile,Projectile):
                self.currentProjectile = projectile
            elif isinstance(projectile,Missile):
                projectile.setTarget(self.tank2)
            sounds.play("projectile")

        else:
            self.tank2.onMouseUp(event)
            projectile = self.tank2.getProjectile()
            projectile.type = "Projectile2"
            self.gameObjects.append(projectile)
            utils.camera.follow(projectile)
            if isinstance(projectile, Projectile):
                self.currentProjectile = projectile
            elif isinstance(projectile, Missile):
                projectile.setTarget(self.tank1)
            sounds.play("projectile")

    def draw(self):
        utils.drawText(Vector2(10, 100), "gravity (Q-E): " + "{:.2f}".format(self.velocity) , (244, 244, 244), 24)
        utils.drawText(Vector2(10, 140), "A/D : move".format(self.velocity), (244, 244, 244), 24)
        utils.drawText(Vector2(10, 180), "hold mouse : shoot".format(self.velocity), (244, 244, 244), 24)
        utils.drawText(Vector2(10, 220), "(left : normal, right: missile)".format(self.velocity),(244, 244, 244), 24)
        utils.drawText(Vector2(10, 260), "W : special".format(self.velocity), (244, 244, 244), 24)
        for obj in self.gameObjects:
            # if utils.distance(obj.pos.x, obj.pos.y, 200, 500) < 50:
            #     continue

            utils.screen.blit(obj.img, (obj.pos.x - utils.camera.pos.x, obj.pos.y - utils.camera.pos.y))
            obj.draw()

        if self.winner == -1:
            utils.drawText(Vector2(500, 100), "Player 1 win!", (244, 23, 23), 43)
        elif self.winner == 1:
            utils.drawText(Vector2(500, 100), "Player 2 win!", (244, 23, 23), 43)

        if self.winner is not None:
            utils.drawText(Vector2(500, 140), "Press 'space' to restart!", (166, 23, 23), 32)
