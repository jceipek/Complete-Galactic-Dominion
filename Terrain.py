import MapObject

class Terrain(MapObject):
    '''This class defines the background objects for the map'''
    def __init__(self, imagePath, colorkey=None):
        MapObject.__init__(self, imagePath, colorkey)
