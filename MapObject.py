import DrawableObject

class MapObject(DrawableObject):
    '''This class will define all of the objects in game play
    that can be placed on the map'''
    def __init__(self, imagePath, colorkey=None):
        DrawableObject.__init__(self, imagePath, colorkey)

        #this is the first initialization of owner
        self.owner=None
        #this is the first initialization of blockable
        self.blockable=False
