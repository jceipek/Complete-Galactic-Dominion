import pygame
import Event
from Listener import Listener
import Terrain
from GameData import ImageBank

class Grid(object):

    def __init__(self,gridSize = (100,100),tileSize=None):
        
        self.terrainImageBank = ImageBank()
        self.terrainImageBank.loadImage('newGrass.png',(255,0,255))
        
        self.gridSize = gridSize
        
        if tileSize is None:
            self.tileWidth,self.tileHeight = self.terrainImageBank.getImage(\
                                        'newGrass.png').get_rect().size
        else:
            self.tileWidth,self.tileHeight = tileSize

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
'''
class InfiniteGrid(Grid):
    """
    A grid that functions like a torus - go off one end and come back on the 
    other side
    """
    def __init__(self,size = (100,100),tileSize=None):
        Grid.__init__(self,size)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        
        tileHeight=self.tileHeight
        tileWidth=self.tileWidth
        
        miny = int(2*screenLoc[1]/tileHeight)-2
        maxy = int(2*(screenLoc[1]+screenSize[1])/tileHeight)+1
        minx = int(screenLoc[0]/tileWidth)-1
        maxx = int((screenLoc[0]+screenSize[0])/tileWidth)+2

        surface.fill((0,0,0))
        
        for y in range(miny,maxy):
            for x in range(minx,maxx):
                
                left = int((x-(y%2)/2.0)*tileWidth-screenLoc[0])
                top = int(y*tileHeight/2.0-screenLoc[1])
                squareLoc=(x%self.gridSize[0],y%self.gridSize[1])
                if not (x%self.gridSize[0]==0 and y%self.gridSize[1]==0):
                    self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))
'''
class InfiniteGrid(Grid):
    """
    A grid that functions like a torus - go off one end and come back on the 
    other side
    """
    def __init__(self,size = (100,100),tileSize=None):
        Grid.__init__(self,size)
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        
        tileHeight=self.tileHeight
        tileWidth=self.tileWidth

        minx=miny=0
        maxx=self.gridSize[0]
        maxy=self.gridSize[1]
        #minx = int(screenLoc[1]/tileHeight)+int(.5*screenLoc[0]/tileWidth)-1
        #miny = minx-int(screenLoc[0]/tileWidth)
        #maxx = minx+int(2.0*screenSize[0]/tileWidth)
        #maxy = miny+int(screenSize[1]/tileHeight)
        print (minx,miny),(maxx,maxy)
        #miny = int(2*screenLoc[1]/tileHeight)-2
        #maxy = int(2*(screenLoc[1]+screenSize[1])/tileHeight)+1
        #minx = int(screenLoc[0]/tileWidth)-1
        #maxx = int((screenLoc[0]+screenSize[0])/tileWidth)+2

        surface.fill((0,0,0))
        font=pygame.font.Font(pygame.font.get_default_font(),12)
        
        for y in range(miny,maxy):
            for x in range(minx,maxx):
                left = int((x-y)/2.0*tileWidth-screenLoc[0])
                top = int((x/2.0+y/2.0)*tileHeight-screenLoc[1])
                self.grid[x%self.gridSize[0],y%self.gridSize[1]].draw(surface,(left,top))

                txt=font.render('(%d, %d)'%(x,y),True,(255,0,0))
                txt.get_rect().center = (left+tileWidth/2,top+tileHeight/2)
                surface.blit(txt,((left+tileWidth/3,top+tileHeight/3),(50,50)))
                
                #left = int((x-(y%2)/2.0)*tileWidth-screenLoc[0])
                #top = int(y*tileHeight/2.0-screenLoc[1])
                #squareLoc=(x%self.gridSize[0],y%self.gridSize[1])
                #if not (x%self.gridSize[0]==0 and y%self.gridSize[1]==0):
                #    self.grid[squareLoc].draw(surface, (left+offset[0], top+offset[1]))


class FiniteGrid(Grid):
    """
    A standard, finite grid (used in most RTS games).
    """
    
    #FIXME FINITE GRIDS WILL NOT WORK NOW BECAUSE OF TMP_Terrain
    
    def __init__(self,size = (100,100),tileSize=None):
        Grid.__init__(self,size,tileSize)
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
