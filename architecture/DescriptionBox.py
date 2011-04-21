from DrawableObjectGroup import DrawableObjectGroup

class DescriptionBox(DrawableObjectGroup):
    
    def __init__(self):
        DrawableObjectGroup.__init__(self,["BarTop.png","BarRight.png","DescBoxCentral.png"])

    def draw(self,screen):
        self.drawObjects(screen)
