from DrawableObject import DrawableObjectGroup

class DescriptionBox(DrawableObjectGroup):
    
    def __init__(self):
        #Format for each tuple is (imagePath, [colorKey, [offset]])
        images = [("BarTop.png",'alpha')]
        images.append(("BarRight.png",'alpha',(325,36)))
        images.append(("DescBoxCentral.png",None,(0,36)))
        DrawableObjectGroup.__init__(self,images,pos=(0,768-36-186))

