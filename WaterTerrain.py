import Terrain

class WaterTerrain(Terrain):
    '''Defines water terrain as a subclass of terrain'''
    def __init__(self, imagePath, colorkey=None):
        Terrain.__init__(self, imagePath, colorkey)
