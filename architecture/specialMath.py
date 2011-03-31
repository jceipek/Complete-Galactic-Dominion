def distance(x1,x2):
    sqSum=0
    for x,y in zip(x1,x2):
        sqSum+=(x-y)**2
    return sqSum**.5
    
def cartToIso(self,coord):
    return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
    
def isoToCart(self,coord):
    return .5*coord[0]-coord[1],.5*coord[0]+coord[1]
