def distance(x1,x2):
    sqSum=0
    for x,y in zip(x1,x2):
        sqSum+=(x-y)**2
    return sqSum**.5
    
def cartToIso(coord):
    return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
    
def isoToCart(coord):
    return .5*coord[0]-coord[1],.5*coord[0]+coord[1]

def hypotenuse(x,y):
    return pow(x**2+y**2,.5)

if __name__ == "__main__":
    print isoToCart((-10,-10))
    print isoToCart((-10,10))
    print isoToCart((10,10))
    print isoToCart((1024,768))
