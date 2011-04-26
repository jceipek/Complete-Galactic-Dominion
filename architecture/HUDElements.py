from DrawableObject import DrawableObjectGroup
from Sign import Sign

class DescriptionBox():
    #The largest HUD element which describes the selected (or hovered?) unit
    #and its properties (those which are player-relevant)
    def __init__(self,pos = (0,768-36-186)):
        #Format for each tuple is (imagePath, [colorKey, [offset]])
        images = [("BarTop.png",'alpha')]
        images.append(("BarRight.png",'alpha',(325,36)))
        images.append(("DescBoxCentral.png",None,(0,36)))
        self.baseLayer = DrawableObjectGroup(images,pos=pos)

    def draw(self,screen):
        self.baseLayer.draw(screen)

class ResourceBar():
    #A bar at the top of the screen indicating the amount of resources the player has on the current world
    def __init__(self,pos = (0,0)):
        images = [("ResourceBar.png", 'alpha')]
        self.baseLayer = DrawableObjectGroup(images,pos=pos)
        self.offset = (30,3)
        self.textField = Sign(200, (pos[0]+self.offset[0],pos[1]+self.offset[1]),fsize = 20)
        self.textField.tcolor=(180,180,0)
        self.setResourceCount(0)

    def setResourceCount(self,val=0):
        self.value = val
        self.textField.clear()
        self.textField.addtext(str(self.value))

    def draw(self,screen):
        #FIXME Add font here
        self.baseLayer.draw(screen)
        self.textField.render(screen)

class UnitBox():
    #One of the tiny boxes displayed when a unit is selected
    
    def __init__(self,entity,pos=(0,0),endCap=False):
        import pygame #FIXME Remove this dependency
        from Overlay import Bar
        
        #Format for each tuple is (imagePath, [colorKey, [offset]])
        images = ["UnitInfoBoxMain.png"]
        if endCap:
            images.append(("UnitInfoBoxRight.png",'alpha',(46,0)))
        self.pos = pos
        self.baseLayer = DrawableObjectGroup(images,pos=self.pos)
        self.entity = entity
        self.thumbnailOffset = (6,10)
        self.thumbnail = pygame.transform.scale(self.entity.image, (36, 36))
        
        self.healthBar = Bar(self.entity.maxHealth,38,5,fullColor=(0,255,0),emptyColor=(30,30,30))

    def draw(self,screen):
        self.healthBar.updateBarWithValue(self.entity.curHealth)
        self.baseLayer.draw(screen)
        screen.blit(self.thumbnail, (self.pos[0]+self.thumbnailOffset[0],self.pos[1]+self.thumbnailOffset[0]))
        self.healthBar.draw(screen,(self.pos[0]+4,self.pos[1]+50))

class SelectedUnitBar():
    #A bar containing the tiny boxes displayed when a unit is selected
    
    def __init__(self):
        self.boxes = []
        self.boxWidth = 46
        self.boxHeight = 63
        self.rowMax = 7
        self.columnMax = 6
        self.rowSpacing = 5
        
    
    def updateWithUnits(self,unitList):
        #Optimally, should be called only when selection changes
        self.boxes = []
        
        unitCount = len(unitList)
        rowNum = 1
        for u in xrange(unitCount-1):
            if (u+1)%self.columnMax == 0:
                self.addBoxForUnit(unitList[u],rowNum,u%self.columnMax,end=True)
                rowNum += 1
            else:
                self.addBoxForUnit(unitList[u],rowNum,u%self.columnMax)
        if unitCount > 0:
            self.addBoxForUnit(unitList[unitCount-1],rowNum,(unitCount-1)%self.columnMax,end=True)
    
    def addBoxForUnit(self,u,row,column,end=False):
        if end:
            self.boxes.append(UnitBox(u,((column*self.boxWidth),(self.rowMax*((self.boxHeight)+self.rowSpacing))-((self.boxHeight)+self.rowSpacing)*(row-1)),endCap=True))
        else:
            self.boxes.append(UnitBox(u,((column*self.boxWidth),(self.rowMax*((self.boxHeight)+self.rowSpacing))-((self.boxHeight)+self.rowSpacing)*(row-1))))
    
    def draw(self,screen):
        for b in self.boxes:
            b.draw(screen)
            
class Notification(Sign):
    def __init__ (self, text='This is a Notification. Consider yourself notified.', pos=(800,0), color=(255, 255, 0), width=200, time=5):
        Sign.__init__(self, width, pos)
        self.addtext(text)
        self.tcolor=color
        self.timeLeft=time*1000
    def draw(self, surface):
        self.render(surface)

class NotificationList():
    """
    List of notifications. Displays multiple notifications which will disappear after some amount of time.
    """
    def __init__(self, pos=(800, 60), width=200, maxLength=5):
        self.notes=[]
        self.pos=pos
        self.width=width
        self.maxLength=maxLength
        
    def add(self, notification):
        self.notes.append(notification)
        notification.offset[0]=self.pos[0]
    def update(self, timeElapsed):
        y=self.pos[1]
        #removes notifications that have timed out
        for n in self.notes:
            n.timeLeft-=timeElapsed
            if n.timeLeft<=0: self.notes.remove(n)
        #keeps list down to the last maxLength number of notifications
        if len(self.notes)>self.maxLength:
            self.notes=self.notes[-1*self.maxLength:]
        #adjusts position of notifications
        for n in self.notes:
            n.offset[1]=y
            y+=n.sy
        
    def draw(self, surf):
        for n in self.notes:
            n.draw(surf)
        

