import pygame
import Event
from Listener import Listener
        
class TMP_Terrain(object):
    def __init__(self,image = None,squareSize = 64,exists = True):
        self.pxSize = squareSize
        self.image = image
        self.exists = exists
        
    def draw(self,surface,pos):
        if self.exists:
            if self.image == None:
                rect = (pos,(self.pxSize,self.pxSize))
                pygame.draw.rect(surface, (0,255,0), rect)
                pygame.draw.rect(surface, (0,0,255), rect, 3)
            else:
                rect = (pos,(self.pxSize,self.pxSize))
                pygame.draw.rect(surface, (0,0,0), rect)

class Grid(object): #SHOULD ACTUALLY INHERIT FROM DRAWABLE OBJECT? SOME SUBCLASS?
    def __init__(self,gridSize = (100,100),\
                       squareSize = 64,\
              terrainObjectDict = None):
        self.gridSize = gridSize
        self.grid = dict()
        self.populateGrid()
        
    def populateGrid(self):
        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):                
                self.grid[(x,y)] = TMP_Terrain(image = None,squareSize = 64)
    
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        #Overriden by Infinite and Finite Grids
        pass


class InfiniteGrid(Grid):
    """
    A grid that functions like a torus - go off one end and come back on the 
    other side
    """
    def __init__(self,size = (100,100),squareSize = 64):
        Grid.__init__(self,size,squareSize)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        squareSize = self.grid[(0,0)].pxSize
        miny = int((screenLoc[1]//squareSize))
        maxy = int(((screenLoc[1]+screenSize[1])//squareSize+1))
        
        minx = int((screenLoc[0]//squareSize))
        maxx = int(((screenLoc[0]+screenSize[0])//squareSize+1))
        
        for y in range(miny,maxy):
            for x in range(minx,maxx):                
                left = int(x*squareSize-screenLoc[0])
                top = int(y*squareSize-screenLoc[1])
                rect = pygame.Rect((left, top), (squareSize,)*2)
                
                squareLoc = (x%self.gridSize[0],y%self.gridSize[1])
                self.grid[squareLoc].draw(surface,\
                    (left+offset[0],top+offset[1]))


class FiniteGrid(Grid):
    """
    A standard, finite grid (used in most RTS games).
    """
    
    def __init__(self,size = (100,100),squareSize = 64):
        Grid.__init__(self,size,squareSize)
        self.emptySquare = TMP_Terrain(exists = False)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        squareSize = self.grid[(0,0)].pxSize
        miny = int((screenLoc[1]//squareSize))
        maxy = int(((screenLoc[1]+screenSize[1])//squareSize+1))
        
        minx = int((screenLoc[0]//squareSize))
        maxx = int(((screenLoc[0]+screenSize[0])//squareSize+1))
        
        for y in range(miny,maxy):
            for x in range(minx,maxx):                
                left = int(x*squareSize-screenLoc[0])
                top = int(y*squareSize-screenLoc[1])
                rect = pygame.Rect((left, top), (squareSize,)*2)
                
                squareLoc = (x,y)
                if squareLoc in self.grid:
                    self.grid[squareLoc].draw(surface,\
                    (left+offset[0],top+offset[1]))
                else:
                    self.emptySquare.draw(surface,\
                    (left+offset[0],top+offset[1]))
