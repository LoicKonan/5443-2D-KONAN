
class Game:

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
