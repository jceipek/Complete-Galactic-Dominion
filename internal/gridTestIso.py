import pygame
import time

def drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc,font):
    #screenLoc is the absolute pixel location of the screen with respect to the
    #grid corners
    
    #miny = int((screenLoc[1]//squareSize))
    #maxy = int(((screenLoc[1]+screenSize[1])//squareSize+1))
    
    #minx = int((screenLoc[0]//squareSize))
    #maxx = int(((screenLoc[0]+screenSize[0])//squareSize+1))
    
    gridSizeY = gridSize
    gridSizeX = gridSize
    tile_width = 128.0
    tile_height = 64.0
    
    d = 0

    miny = int(2*screenLoc[1]/tile_height)-2
    maxy = int(2*(screenLoc[1]+screenSize[1])/tile_height)+1
    minx = int(screenLoc[0]/tile_width)-1
    maxx = int((screenLoc[0]+screenSize[0])/tile_width)+2
    
    for y in range(miny,maxy):
        for x in range(minx,maxx):
            left = int((x-(y%2)/2.0)*tile_width-screenLoc[0])
            top = int(y*tile_height/2.0-screenLoc[1])
            rect = pygame.Rect((left, top), (tile_width,tile_height))
            #pygame.draw.rect(screen, color, rect)
            screen.blit(grid[(x%gridSize,y%gridSize)][0],rect)
            '''
            print 'rect: ',rect
            print 'x: ', x
            print 'y: ', y
            print 'left: ', left
            print 'top: ', top
            print 'minx: ', minx
            print 'maxx:', maxx
            print 'miny: ', miny
            print 'maxy:', maxy 
            txt = font.render(str((x,y)), False, (255,0,0))
            txtbound = txt.get_rect()
            txtbound.center = (left+tile_width / 2.0,top+tile_height / 2.0)
            screen.blit(txt, txtbound)
            '''

    """
    for i in range(0, gridSizeX):
        if i%2 == 1: #If it is odd
            offset_x = tile_width / 2.0
        else:
            offset_x = 0

        for j in range(0,gridSizeY):
            x = j * tile_width + offset_x - screenLoc[0]
            y = i * tile_height / 2.0 - screenLoc[1]
            
            rect = pygame.Rect((x, y), (tile_width,tile_height))
            screen.blit(grid[(j,i)][0],rect)
        
            d+=1
            #txt = font.render(str(d), False, (255,0,0))
            txt = font.render(str((j,i)), False, (255,0,0))
            txtbound = txt.get_rect()
            txtbound.center = (x+tile_width / 2.0,y+tile_height / 2.0)
            screen.blit(txt, txtbound)
    """
            
    """
    for y in range(miny,maxy):
        for x in range(minx,maxx):
            #if grid[(x%gridSize,y%gridSize)] == 0:
            #    color = (0,0,0)
            #else:
            #    color = (255,255,255)
            
            left = int(x*squareSize-screenLoc[0])
            top = int(y*squareSize-screenLoc[1])
            rect = pygame.Rect((left, top), (squareSize,)*2)
            #pygame.draw.rect(screen, color, rect)
            
            screen.blit(grid[(x%gridSize,y%gridSize)],rect)
               
       """
gridSize = 5
squareSize = 64

screenSize = (width, height) = (1024, 768)
screenLoc = [0.0, 0.0]

deadZoneSize = (width-200,height-200)
deadZone = pygame.Rect((0, 0), deadZoneSize)
deadZone.center = (width/2.0,height/2.0)
scrollSpeed = 1

RUNNING = True
pygame.init()
screen = pygame.display.set_mode(screenSize)
screenZone = screen.get_rect()
ms_elapsed = 1

font = pygame.font.Font(pygame.font.get_default_font(), 16)
txt = font.render("FPS: ***", True, (255,255,255))
txtbound = txt.get_rect()

grid = dict()

grass1 = pygame.image.load("GoodIsoGrass.png").convert_alpha()
grass2 = pygame.image.load("GoodIsoGrass.png").convert_alpha()
building = pygame.image.load("testBuilding.png").convert_alpha()

from random import choice,seed
seed(44)
grass = [grass1,grass2]
for y in range(gridSize):
    
    for x in range(gridSize):
        
        square = choice(grass)
        unit = choice([None,building])
        grid[(x,y)] = (square,unit)

hud1 = pygame.image.load("HUD_sism.png").convert_alpha()
hudZone1 = hud1.get_rect()
hud2 = pygame.image.load("HUD_sibottom.png").convert()
hudZone2 = hud2.get_rect()
hudZone2.bottom = height

maxFPS = 60

# Initialize a game clock
gameClock = pygame.time.Clock()

while RUNNING:
    ms_elapsed = gameClock.tick(maxFPS)
    
    screen.fill((0,0,0))
    
    mPos = pygame.mouse.get_pos()
    #screenLoc = (mPos[0]-screenSize[0]/2.0+0.05,mPos[1]-screenSize[1]/2.0)
    if screenZone.collidepoint(mPos):
        dx = (mPos[0]-deadZone.center[0])
        dy = (mPos[1]-deadZone.center[1])
        
        # distance formula
        calcDistance = lambda a,b: pow(a**2 + b**2, 0.5)
        
        magnitude=calcDistance(dx,dy)
        dirx=dx/magnitude #x component of unit direction
        diry=dy/magnitude #y component of unit direction

        dx=max([0, abs(dx)-deadZoneSize[0]/2.0])
        dy=max([0, abs(dy)-deadZoneSize[1]/2.0])

        speedCoeff=calcDistance(dx,dy)/(width-deadZoneSize[0])*2.0
        screenLoc[0] += dirx*scrollSpeed*speedCoeff*ms_elapsed
        screenLoc[1] += diry*scrollSpeed*speedCoeff*ms_elapsed
    
    drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc,font)
    
    pygame.draw.rect(screen, (150,150,0), deadZone, 3)
    
    #screen.blit(hud1, hudZone1)
    #screen.blit(hud2, hudZone2)
    
    txt = font.render("FPS: %s"%int(gameClock.get_fps()), True, (0,150,150))
    screen.blit(txt, txtbound)
    
    for event in pygame.event.get():
        print event
        if event.type == pygame.QUIT:
            RUNNING = False
            
    pygame.display.flip()
                
pygame.quit()
