import pygame
import Event
from Listener import Listener
import Terrain

class TMP_Terrain(object):
    def __init__(self,image = None,tile_height = 64, tile_width= 128, exists = True):
        self.image=pygame.image.load('newGrass.png') #FIXME FINITE GRIDS WILL NOT WORK NOW
        self.image.set_colorkey((255,255,255))
        self.height=tile_height
        self.width=tile_width
        #self.image = image
        self.exists = exists
        
    def draw(self,surface,pos):
        if self.exists:
            if self.image == None:
                rect = (pos,(self.height,self.width))
                pygame.draw.rect(surface, (0,255,0), rect)
                pygame.draw.rect(surface, (0,0,255), rect, 3)
            else:
                rect = (pos,(self.height,self.width))
                #pygame.draw.rect(surface, (0,0,0), rect)
                surface.blit(self.image, rect)

class Grid(object): #SHOULD ACTUALLY INHERIT FROM DRAWABLE OBJECT? SOME SUBCLASS?
    def __init__(self,gridSize = (100,100),\
                       tile_height= 64, tile_width=128,\
              terrainObjectDict = None):
        self.gridSize = gridSize
        self.grid = dict()
        self.populateGrid()
        
    def populateGrid(self):
        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):                
                self.grid[(x,y)] = TMP_Terrain(image = None,tile_height = 64, tile_width=128)
                #self.grid[(x,y)] = Terrain.Grass('newGrass.png','alpha')
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        #Overriden by Infinite and Finite Grids
        pass


class InfiniteGrid(Grid):
    """
    A grid that functions like a torus - go off one end and come back on the 
    other side
    """
    def __init__(self,size = (100,100),tile_height= 64, tile_width=128):
        Grid.__init__(self,size,tile_height, tile_width)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):

        tile_height= self.grid[(0,0)].height
        tile_width= self.grid[(0,0)].width
        miny = int(2*screenLoc[1]/tile_height)-2
        maxy = int(2*(screenLoc[1]+screenSize[1])/tile_height)+1
        minx = int(screenLoc[0]/tile_width)-1
        maxx = int((screenLoc[0]+screenSize[0])/tile_width)+2

        for y in range(miny,maxy):
            for x in range(minx,maxx):
                left = int((x-(y%2)/2.0)*tile_width-screenLoc[0])
                top = int(y*tile_height/2.0-screenLoc[1])
                squareLoc=(x%self.gridSize[0],y%self.gridSize[1])

                self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))

class FiniteGrid(Grid):
    """
    A standard, finite grid (used in most RTS games).
    """
    
    #FIXME FINITE GRIDS WILL NOT WORK NOW BECAUSE OF TMP_Terrain
    
    def __init__(self,size = (100,100),tile_height=64, tile_width=128):
        Grid.__init__(self,size,tile_height=64, tile_width=128)
        self.emptySquare = TMP_Terrain(exists = False)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        tile_height = self.grid[(0,0)].height
        tile_width = self.grid[(0,0)].width
        miny = int(2*screenLoc[1]/tile_height)-2
        maxy = int(2*(screenLoc[1]+screenSize[1])/tile_height)+1
        minx = int(screenLoc[0]/tile_width)-1
        maxx = int((screenLoc[0]+screenSize[0])/tile_width)+2
        """
        for y in range(miny,maxy):
            for x in range(minx,maxx):                
                left = int(x*squareSize-screenLoc[0])
                top = int(y*squareSize-screenLoc[1])
                rect = pygame.Rect((left, top), (squareSize,)*2)
        """
        for y in range(miny,maxy):
            for x in range(minx,maxx):
                left = int((x-(y%2)/2.0)*tile_width-screenLoc[0])
                top = int(y*tile_height/2.0-screenLoc[1])
                squareLoc=(x,y)

                if squareLoc in self.grid:
                    self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))
                else:
                    self.emptySquare.draw(surface,\
                    (left+offset[0],top+offset[1]))

if __name__ == '__main__':
    pass
