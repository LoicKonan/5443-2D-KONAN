from objects.GameObject import GameObject
from utils.assets_manager import assetsManager


class Bullets(GameObject):

    def __init__(self,pos):
        super(Bullets, self).__init__(pos,assetsManager.get("bullets"))