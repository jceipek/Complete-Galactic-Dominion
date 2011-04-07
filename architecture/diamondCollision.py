def collideRectDiamond(self,rect1,diamond):
    left,top=rect1.topleft
    right,bottom=rect1.bottomright
    bottom,top=sorted((top,bottom))
    left,right=sorted((left,right))
    
    #pHigh,pLow,pLeft,pRight=diamond
    
    pRight=max(diamond)
    pLeft=min(diamond)
    pHigh=pLow=diamond[0]
    for i in range(1,len(diamond)):
        if diamond[i][1]>pHigh[1]:
            pHigh=diamond[i]
        if diamond[i][1]<pLow[1]:
            pLow=diamond[i]
    
    def line(p1,p2,x):
        slope=(p1[1]-p2[1])/(p1[0]-p2[0])
        return slope*(x-p1[0])+p1[1]
    
    if line(pHigh,pLeft,right)<=bottom:
        return False
    if line(pLow,pRight,left)>=top:
        return False
    if line(pHigh,pRight,left)<=bottom:
        return False
    if line(pLow,pLeft,right)>=top:
        return False
    return True
    
import pygame

r=pygame.rect(1,1,0,0)
diam=((1,0),(0,1),(-1,0),(0,-1))
print collideRectDiamond

