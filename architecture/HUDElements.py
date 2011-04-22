from DrawableObject import DrawableObjectGroup

class DescriptionBox():
    #The largest HUD element which describes the selected (or hovered?) unit
    #and its properties (those which are player-relevant)
    def __init__(self):
        #Format for each tuple is (imagePath, [colorKey, [offset]])
        images = [("BarTop.png",'alpha')]
        images.append(("BarRight.png",'alpha',(325,36)))
        images.append(("DescBoxCentral.png",None,(0,36)))
        self.baseLayer = DrawableObjectGroup(images,pos=(0,768-36-186))

    def draw(self,screen):
        self.baseLayer.draw(screen)

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
        print "New"
        print unitCount
        print len(unitList)
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
