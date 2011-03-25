from MapObject import MapObject

class Terrain(MapObject):
    """
    Defines all background objects for the map.
    First class to implement the exists attribute, which defines
    whether or not the terrain is a part of the map, or a placeholder
    in a finite grid.
    """
    def __init__(self, imagePath=None, colorkey=None, exists=True):

        MapObject.__init__(self, imagePath, x=0, y=0, colorkey=colorkey)
        self.exists = True
        
    def draw(self,surface,drawCorner):
        if self.exists:
            if self.image == None:
                rect = (drawCorner,(self.rect.height,rect.self.width))
                pygame.draw.rect(surface, (0,255,0), self.rect)
                pygame.draw.rect(surface, (0,0,255), self.rect, 3)
            else:
                #rect = (pos,(self.height,self.width))
                #pygame.draw.rect(surface, (0,0,0), rect)
                surface.blit(self.image, self.rect.move(drawCorner))
        else:
            # Currently does not do anything if self.exists == False
            pass

class Grass(Terrain):
    """
    Defines grass terrain as a subclass of terrain
    """
    def __init__(self, imagePath, colorkey=None):
        if imagePath == None:
            imagePath = 'newGrass.png'
        Terrain.__init__(self, imagePath, colorkey, exists=True)
