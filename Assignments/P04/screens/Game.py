class Game:
    def __init__(self):
        pass

    def update(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def onKeyDown(self, key):
        raise NotImplementedError()

    def onKeyUp(self, key):
        raise NotImplementedError()

    def onMouseDown(self, event):
        raise NotImplementedError()

    def onMouseUp(self, event):
        raise NotImplementedError()

    def onMouseWheel(self, event):
        pass