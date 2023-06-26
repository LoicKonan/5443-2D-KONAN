from objects.GameObject import GameObject


class Enemy(GameObject):
    def __init__(self,pos):
        super().__init__(pos,None)