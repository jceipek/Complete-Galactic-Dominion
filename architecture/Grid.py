import pygame
import Event
from Listener import Listener
import Terrain

class Grid(object):

    def __init__(self,gridSize = (100,100),tileSize=None):
        
        self.gridSize = gridSize
        self.tileWidth, self.tileHeight = (0,0)

        self.grid = dict()
        self.populateGrid()
        
    def populateGrid(self):
        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):
                self.grid[(x,y)] = Terrain.Grass('newGrass.png',(255,0,255))
        self.tileWidth, self.tileHeight = self.grid[(0,0)].rect.size
        
    def draw(self,surface,screenLoc,screenSize,offset=(0,0)):
        #Overriden by Infinite and Finite Grids
        pass
        
    def getGridDimensions(self):
        return self.gridSize[0]*self.tileWidth,self.gridSize[1]*self.tileHeight
        
    def cartToIso(self,coord):
        return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
        
    def isoToCart(self,coord):
        return .5*coord[0]-coord[1],.5*coord[0]+coord[1]
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
        
        trect = pygame.Rect(screenLoc,screenSize)
        left,top = trect.topleft
        right,bottom = trect.bottomright
        
        screenLeftTop = self.isoToCart((left,top))
        screenRightTop = self.isoToCart((right,top))
        screenRightBottom = self.isoToCart((right,bottom))
        screenLeftBottom = self.isoToCart((left,bottom))
        
        #print screenLeftTop[0],screenRightTop[0],screenRightBottom[0],screenLeftBottom[0]
        
        minx = int(screenLeftBottom[0]/tileHeight)-2
        maxx = int(screenRightTop[0]/tileHeight)+2
        miny = int(screenLeftTop[1]/tileHeight)-2
        maxy = int(screenRightBottom[1]/tileHeight)+1
        
        """ #create the font that will draw the coordinates on the square. <fps
        font=pygame.font.Font(pygame.font.get_default_font(),12)"""
        
        surface.fill((0,0,0));
        
        for y in range(miny,maxy):
            for x in range(minx,maxx):
                
                #find the left and top position of the image relative to the screen in iso
                left = int((y+x)/2.0*tileWidth-screenLoc[0])
                top = int((y-x)/2.0*tileHeight-screenLoc[1])
                
                if pygame.Rect((left,top),(tileWidth,tileHeight)).\
                colliderect((0,0),screenSize):
                    self.grid[x%self.gridSize[0],y%self.gridSize[1]].\
                    draw(surface,(left,top))
                
                """ #Comment out this line to test grid wrapping
                if pygame.Rect((left,top),(tileWidth,tileHeight)).\
                colliderect((0,0),screenSize):
                    if not(x%self.gridSize[0] == 2 and y%self.gridSize[1] == 2):
                     self.grid[x%self.gridSize[0],y%self.gridSize[1]].\
                     draw(surface,(left,top))#"""

                #draw the text to the square
                #txt=font.render('(%d, %d)'%(x,y),True,(255,0,0))
                #txt.get_rect().center = (left+tileWidth/2,top+tileHeight/2)
                #surface.blit(txt,((left+tileWidth/3,top+tileHeight/3),(50,50)))

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
