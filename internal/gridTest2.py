import pygame

def drawVisible(screen,grid,gridSize,squareSize,mapSize,screenLoc,font):
	#screenLoc is the absolute pixel location of the screen with respect to the
	#grid corners
	
	miny = int((screenLoc[1]//squareSize))
	maxy = int(((screenLoc[1]+mapSize[1])//squareSize+1))
	
	minx = int((screenLoc[0]//squareSize))
	maxx = int(((screenLoc[0]+mapSize[0])//squareSize+1))
	
	for y in range(miny,maxy):
		for x in range(minx,maxx):
			
			left = int(x*squareSize-screenLoc[0])
			top = int(y*squareSize-screenLoc[1])
			rect = pygame.Rect((left, top), (squareSize,)*2)
			
			screen.blit(grid[(x%gridSize,y%gridSize)],rect)
			
			"""
			txt = font.render(str((x%gridSize,y%gridSize)), True, (255,0,0))
			txtbound = txt.get_rect()
			txtbound.center = (left+squareSize/2,top+squareSize/2)
   			screen.blit(txt, txtbound)
   			#"""
   			
gridSize = 100
squareSize = 64

screenSize = (screenWidth, screenHeight) = (1024, 768)
screenLoc = [0.0, 0.0]

mapSize = (mapWidth, mapHeight) = (1024, 568)
mapLoc = [0.0, 0.0]
gameZone = pygame.Rect((0,0),mapSize)

deadZoneSize = (mapWidth-200,mapHeight-200)
deadZone = pygame.Rect((0, 0), deadZoneSize)
deadZone.center = (mapWidth/2.0,mapHeight/2.0)

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

grass1 = pygame.image.load("grass1.png").convert()
grass2 = pygame.image.load("grass2.png").convert()

from random import choice,seed
seed(44)
grass = [grass1,grass2]
for y in range(gridSize):
	
	for x in range(gridSize):
		
		square = choice(grass)
		"""
		if (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1):
			#checker black
			square = grass1
		else:
			#checker white
			square = grass2
		"""
		
		grid[(x,y)] = square

hud1 = pygame.image.load("HUD_sism.png").convert_alpha()
hudZone1 = hud1.get_rect()
hud2 = pygame.image.load("HUD_sibottom.png").convert()
hudZone2 = hud2.get_rect()
hudZone2.bottom = screenHeight

maxFPS = 100

# Initialize a game clock
gameClock = pygame.time.Clock()

while RUNNING:
	ms_elapsed = gameClock.tick(maxFPS)
	
	mPos = pygame.mouse.get_pos()
	#screenLoc = (mPos[0]-screenSize[0]/2.0+0.05,mPos[1]-screenSize[1]/2.0)
	if gameZone.collidepoint(mPos):
		dx = (mPos[0]-deadZone.center[0])
		dy = (mPos[1]-deadZone.center[1])
		magnitude=pow(dx**2+dy**2,0.5) #distance from center
		dirx=dx/magnitude #x component of unit direction
		diry=dy/magnitude #y component of unit direction

		dx=max([0, abs(dx)-deadZoneSize[0]/2.0])
		dy=max([0, abs(dy)-deadZoneSize[1]/2.0])

		speedCoeff=pow(dx**2+dy**2,0.5)/(mapWidth-deadZoneSize[0])*2.0
		screenLoc[0] += dirx*scrollSpeed*speedCoeff*ms_elapsed
		screenLoc[1] += diry*scrollSpeed*speedCoeff*ms_elapsed
		
		#print speedCoeff
		#print mPos
	
	drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc,font)
	
	pygame.draw.rect(screen, (150,150,0), deadZone, 3)
	
	screen.blit(hud1, hudZone1)
	screen.blit(hud2, hudZone2)
	
	txt = font.render("FPS: %s"%int(gameClock.get_fps()), True, (0,150,150))
	screen.blit(txt, txtbound)
	
	for event in pygame.event.get():
                print event
		if event.type == pygame.QUIT:
			RUNNING = False
	
	pygame.display.flip()
	            
pygame.quit()
