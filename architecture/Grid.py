import pygame
import Event
from Listener import Listener
import Terrain
from GameData import ImageBank

class Grid(object): #SHOULD ACTUALLY INHERIT FROM DRAWABLE OBJECT? SOME SUBCLASS?

    def __init__(self,gridSize = (100,100),\
                       tileHeight= 64, tileWidth=128,\
              terrainObjectDict = None):
        
        self.terrainImageBank = ImageBank()
        self.terrainImageBank.loadImage('newGrass.png',(255,0,255))
        
        self.gridSize = gridSize
        self.tileHeight = tileHeight
        self.tileWidth = tileWidth
        self.grid = dict()
        self.populateGrid()
        
    def populateGrid(self):
        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):
                self.grid[(x,y)] = Terrain.Grass(self.terrainImageBank.getImage('newGrass.png'))
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        #Overriden by Infinite and Finite Grids
        pass
        
    def getGridDimensions(self):
        return self.gridSize[0]*self.tileWidth,self.gridSize[1]*self.tileHeight

class InfiniteGrid(Grid):
    """
    A grid that functions like a torus - go off one end and come back on the 
    other side
    """
    def __init__(self,size = (100,100),tileHeight= 64, tileWidth=128):
        Grid.__init__(self,size,tileHeight,tileWidth)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        
        tileHeight= self.grid[(0,0)].rect.height
        tileWidth= self.grid[(0,0)].rect.width
        miny = int(2*screenLoc[1]/tileHeight)-2
        maxy = int(2*(screenLoc[1]+screenSize[1])/tileHeight)+1
        minx = int(screenLoc[0]/tileWidth)-1
        maxx = int((screenLoc[0]+screenSize[0])/tileWidth)+2

        for y in range(miny,maxy):
            for x in range(minx,maxx):
                left = int((x-(y%2)/2.0)*tileWidth-screenLoc[0])
                top = int(y*tileHeight/2.0-screenLoc[1])
                squareLoc=(x%self.gridSize[0],y%self.gridSize[1])

                self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))

class FiniteGrid(Grid):
    """
    A standard, finite grid (used in most RTS games).
    """
    
    #FIXME FINITE GRIDS WILL NOT WORK NOW BECAUSE OF TMP_Terrain
    
    def __init__(self,size = (100,100),tileHeight=64, tileWidth=128):
        Grid.__init__(self,size,tileHeight=64, tileWidth=128)
        self.emptySquare = TMP_Terrain(exists = False)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        tileHeight = self.grid[(0,0)].height
        tileWidth = self.grid[(0,0)].width
        miny = int(2*screenLoc[1]/tileHeight)-2
        maxy = int(2*(screenLoc[1]+screenSize[1])/tileHeight)+1
        minx = int(screenLoc[0]/tileWidth)-1
        maxx = int((screenLoc[0]+screenSize[0])/tileWidth)+2
        """
        for y in range(miny,maxy):
            for x in range(minx,maxx):                
                left = int(x*squareSize-screenLoc[0])
                top = int(y*squareSize-screenLoc[1])
                rect = pygame.Rect((left, top), (squareSize,)*2)
        """
        for y in range(miny,maxy):
            for x in range(minx,maxx):
                left = int((x-(y%2)/2.0)*tileWidth-screenLoc[0])
                top = int(y*tileHeight/2.0-screenLoc[1])
                squareLoc=(x,y)

                if squareLoc in self.grid:
                    self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))
                else:
                    self.emptySquare.draw(surface,\
                    (left+offset[0],top+offset[1]))

if __name__ == "__main__":
    pass
