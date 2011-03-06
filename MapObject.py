import DrawableObject

class MapObject(DrawableObject):
    '''This class will define all of the objects in game play
    that can be placed on the map'''
    def __init__(self):
        DrawableObject.__init__(self)
        owner=None#this is the first initialization of owner
        blockable=False#this is the first initialization of blockable
