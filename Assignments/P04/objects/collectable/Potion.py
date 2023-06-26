from objects.GameObject import GameObject
from utils.assets_manager import assetsManager


class Potion(GameObject):

    def __init__(self,pos):
        super(Potion, self).__init__(pos,assetsManager.get("hp"))