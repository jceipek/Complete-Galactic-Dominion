from DrawableObject import DrawableObject
import pygame

class MapObject(DrawableObject, pygame.sprite.Sprite):
    '''This class will define all of the objects in game play
    that can be placed on the map'''
    def __init__(self, imagePath, x, y, colorkey=None):
        # sets image and rect attributes
        # First class to inherit from Sprite
        DrawableObject.__init__(self, imagePath, colorkey)
        
        self.rect.topleft = self.pos = (x,y)

        # this is the first initialization of owner
        self.owner=None # default to no owner
        
        # this is the first initialization of blockable
        # determines whether or not an object can be walked through
        self.blockable=False
        
        # rectangle used EXCLUSIVELY for collision detection
        # defaults to the image rectangle
        # NOTE: update methods need to move collRect with rect!
        self.collRect = self.rect
