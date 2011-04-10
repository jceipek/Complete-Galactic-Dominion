import pygame
from DrawableObject import DrawableObject

def offsetFromDeg(deg,rad):
    from math import cos
    from math import sin
    x = cos(deg)*rad
    y = sin(deg)*rad
    return (x,y)
    
def degFromOffset(offset):
    from math import atan2
    return(atan2(offset[1],offset[0]))
    
def findIndex(deg,count,degOffset):
    from math import degrees
    # Returns tuple.  First element is div, second is mod!  (How surprising).  div should be index + 0 or 1.
    indexRaw, indexMod = divmod(deg%(2.0*3.14159),degOffset)
    if indexMod > degOffset/2.0:
        index = int((indexRaw + 1)%count)
    else:
        index = int(indexRaw)
    return index

class RMenu():
    """
    A radial menu containing RMenuItems
    @param loc: location of the menu
    @param rad: radius of the menu
    @param visible: whether the menu can be seen (it is open)
    @param root: a list of the menu items contained in the menu
    """
    def __init__(self,loc = (0,0),rad = 80,minDist=15,title=None):
        self.root = []
        self.loc = loc
        self.mousePos = loc
        self.rad = rad
        self.minDist = minDist
        self.visible = False
        
    def addItem(self,item):
        self.root.append(item)
    
    def open(self,loc):
        self.loc = loc
        self.mousePos = loc
        self.visible = True
        
    def select(self,loc):
        if self.visible:
            offset = (loc[0] - self.loc[0], loc[1] - self.loc[1])
            from math import hypot
            dist = hypot(offset[0],offset[1])
            if dist >= self.minDist:
                deg = degFromOffset(offset)
                count = len(self.root)
                degOffset = (2.0*3.14159)/count
                index = findIndex(deg,count,degOffset)
                if self.root[index].submenu:
                    self.root[index].submenu.select(loc)
                else:
                    self.root[index].select()
            self.close()
                 
    def close(self):
        self.visible = False
        count = len(self.root)
        for i in xrange(count):
            if self.root[i].submenu:
                if self.root[i].submenu.visible:
                    self.root[i].submenu.close()
        
    def update(self,loc):    
        if self.visible:
            self.mousePos = loc
            offset = (self.mousePos[0] - self.loc[0], self.mousePos[1] - self.loc[1])
            from math import hypot
            dist = hypot(offset[0],offset[1])
            count = len(self.root)
            if dist >= self.minDist:
                deg = degFromOffset(offset)
                degOffset = (2.0*3.14159)/count
                index = findIndex(deg,count,degOffset)
                childOffset = offsetFromDeg(index*degOffset,self.rad)
                childLoc = (childOffset[0]+self.loc[0],childOffset[1]+self.loc[1])
                self.root[index].update(childLoc,loc)
                
                #Close all other submenus:
                for i in xrange(count):
                    if not i == index:
                        if self.root[i].submenu:
                            if self.root[i].submenu.visible:
                                self.root[i].submenu.close()
            else:
                for i in xrange(count):
                    if self.root[i].submenu:
                        if self.root[i].submenu.visible:
                            self.root[i].submenu.close()              

    def draw(self,surf):
        if self.visible:
            count = len(self.root)

            if count > 0:
                #Divide items evenly along a circle
                degOffset = (2.0*3.14159)/count
                for i in xrange(count):
                    childOffset = offsetFromDeg(i*degOffset,self.rad)
                    childLoc = (childOffset[0]+self.loc[0],childOffset[1]+self.loc[1])
                    self.root[i].draw(surf,childLoc)
                    
                offset = (self.mousePos[0] - self.loc[0], self.mousePos[1] - self.loc[1])
                from math import hypot
                dist = hypot(offset[0],offset[1])
                if dist >= self.minDist:
                    deg = degFromOffset(offset)
                    index = findIndex(deg,count,degOffset)
                    #Draw highlight
                    childOffset = offsetFromDeg(index*degOffset,self.rad)
                    childLoc = (childOffset[0]+self.loc[0],childOffset[1]+self.loc[1])
                    pygame.draw.line(surf, (100,100,100), self.loc, childLoc,3)
                    
                    if self.root[index].submenu:
                        self.root[index].submenu.draw(surf)
                    else:
                        self.root[index].highlight(surf,childLoc)
      
class RMenuItem(DrawableObject):
    """
    A menu item suitable for use in an RMenu
    @param menu: The menu that contains the item
    """
    def __init__(self,menu,image = "orbBlack.png",imageKey = -1,title = 'None',size = 32,col = (0,0,255)):

        DrawableObject.__init__(self,image,imageKey) #Should be different for each item
        
        self.title = title
        self.size = size
        self.color = col
        self.menu = menu
        self.submenu = None
         
    def addSubmenu(self,menu):
        self.submenu = menu
    
    def draw(self,surf,loc):
        self.rect.center=loc
        surf.blit(self.image,self.rect)
        if self.submenu:
            self.submenu.draw(surf)
        
    def select(self):
        print self.title
        
    def update(self,loc,mouseLoc):
        if self.submenu:
            if not self.submenu.visible:
                self.submenu.open(loc)
            else:
                self.submenu.update(mouseLoc)
    
    def highlight(self,surf,loc):
        pygame.draw.circle(surf, self.color, loc, self.size,2)
        
        
if __name__ == "__main__":
    """
    Usage example
    """
    pygame.init()
    resolution = (width,height) = (640,480)
    displaySurface = pygame.display.set_mode(resolution)
    RUNNING = True
    
    #Set up the test menu:
    menu = RMenu()
    menu2 = RMenu()
    menu3 = RMenu()
    menu4 = RMenu()
    
    item1 = RMenuItem(menu,image = "orbQBlack.png",col = (255,0,0),title = "Red")
    item2 = RMenuItem(menu,image = "orbQBlack.png")
    item3 = RMenuItem(menu,image = "orbPurpleBlack.png",col = (255,0,255),title = "Purple")
    item1.addSubmenu(menu4)
    item2.addSubmenu(menu2)
    
    menu.addItem(item1)
    menu.addItem(item2)
    menu.addItem(item3)
    
    item4 = RMenuItem(menu,image = "orbBlueBlack.png",col = (0,0,255),title = "Blue")
    item5 = RMenuItem(menu,image = "orbQBlack.png")
    item5.addSubmenu(menu3)
    
    menu2.addItem(item4)
    menu2.addItem(item5)
    
    item6 = RMenuItem(menu,image = "orbWhiteBlack.png",col = (255,255,255),title = "White")
    item7 = RMenuItem(menu,image = "orbRedBlack.png",col = (255,0,0),title = "Red#2")
    item8 = RMenuItem(menu,image = "orbPurpleBlack.png",col = (255,0,255),title = "Purple#2") 
    
    menu3.addItem(item6)
    menu3.addItem(item7)
    menu3.addItem(item8)
    
    item9 = RMenuItem(menu,image = "orbRedBlack.png",col = (255,0,0),title = "Red#3")
    item10 = RMenuItem(menu,image = "orbRedBlack.png",col = (255,0,0),title = "Red#4")
    item11 = RMenuItem(menu,image = "orbRedBlack.png",col = (255,0,0),title = "Red#5")
    item12 = RMenuItem(menu,image = "orbRedBlack.png",col = (255,0,0),title = "Red#6")

    menu4.addItem(item9)
    menu4.addItem(item10)
    menu4.addItem(item11)
    menu4.addItem(item12)
    
    while RUNNING:
    
        displaySurface.fill((0,0,0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    print "Menu opened"
                    menu.open(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    print "Menu closed"
                    menu.select(event.pos)
            if event.type == pygame.MOUSEMOTION:
                menu.update(event.pos)
        menu.draw(displaySurface)    
        pygame.display.flip()
                    
