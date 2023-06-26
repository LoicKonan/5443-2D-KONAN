from objects.GameObject import GameObject


class Projectile(GameObject):
    def __init__(self,pos):
        super().__init__(pos,None)