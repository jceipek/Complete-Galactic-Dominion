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
    
    def __init__(self,pos=(0,0)):
        #Format for each tuple is (imagePath, [colorKey, [offset]])
        images = ["UnitInfoBoxMain.png"]
        images.append(("UnitInfoBoxRight.png",'alpha',(46,0)))
        self.pos = pos
        self.baseLayer = DrawableObjectGroup(images,pos=self.pos)

    def draw(self,screen):
        self.baseLayer.draw(screen)

class SelectedUnitBar():
    #One of the tiny boxes displayed when a unit is selected
    
    def __init__(self):
        self.test = UnitBox((0,200))
        
    def draw(self,screen):
        self.test.draw(screen)
