import pygame

def drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc,font):
	#screenLoc is the absolute pixel location of the screen with respect to the
	#grid corners
	
	miny = int((screenLoc[1]//squareSize))
	maxy = int(((screenLoc[1]+screenSize[1])//squareSize+1))
	
	minx = int((screenLoc[0]//squareSize))
	maxx = int(((screenLoc[0]+screenSize[0])//squareSize+1))
	
	for y in range(miny,maxy):
		for x in range(minx,maxx):
			#if grid[(x%gridSize,y%gridSize)] == 0:
			#	color = (0,0,0)
			#else:
			#	color = (255,255,255)
			
			left = int(x*squareSize-screenLoc[0])
			top = int(y*squareSize-screenLoc[1])
			rect = pygame.Rect((left, top), (squareSize,)*2)
			#pygame.draw.rect(screen, color, rect)
			
			screen.blit(grid[(x%gridSize,y%gridSize)],rect)
			
			txt = font.render(str((x%gridSize,y%gridSize)), True, (255,0,0))
			txtbound = txt.get_rect()
			txtbound.center = (left+squareSize/2,top+squareSize/2)
   			screen.blit(txt, txtbound)

gridSize = 100
squareSize = 64

screenSize = (width, height) = (640, 480)
screenLoc = [0.0, 0.0]
deadZoneSize = (width-200,height-200)
deadZone = pygame.Rect((0, 0), deadZoneSize)
deadZone.center = (width/2.0,height/2.0)
scrollSpeed = 15

RUNNING = True
pygame.init()
screen = pygame.display.set_mode(screenSize)
screenZone = screen.get_rect()
ms_elapsed = pygame.time.get_ticks()

font = pygame.font.Font(pygame.font.get_default_font(), 12)
txt = font.render("FPS: ***", True, (255,255,255))
txtbound = txt.get_rect()

grid = dict()

grass1 = pygame.image.load("grass1.png").convert()
grass2 = pygame.image.load("grass2.png").convert()

for y in range(gridSize):
	for x in range(gridSize):
		if (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1):
			#checker black
			square = grass1
		else:
			#checker white
			square = grass2
		grid[(x,y)] = square


while RUNNING:
	last_time = pygame.time.get_ticks()
	
	screen.fill((255,0,0)) #not necessary if we draw everywhere
	
	mPos = pygame.mouse.get_pos()
	#screenLoc = (mPos[0]-screenSize[0]/2.0+0.05,mPos[1]-screenSize[1]/2.0)
	if screenZone.collidepoint(mPos):
		dx = (mPos[0]-deadZone.center[0])
		dy = (mPos[1]-deadZone.center[1])
		magnitude=pow(dx**2+dy**2,0.5) #distance from center
		dirx=dx/magnitude #x component of unit direction
		diry=dy/magnitude #y component of unit direction

		dx=abs(dx)-deadZoneSize[0]/2.0
		dy=abs(dy)-deadZoneSize[1]/2.0
		if dx<0: dx=0
		if dy<0: dy=0
		speedCoeff=pow(dx**2+dy**2,0.5)/(width-deadZoneSize[0])*2.0
		screenLoc[0] += dirx*scrollSpeed*speedCoeff
		screenLoc[1] += diry*scrollSpeed*speedCoeff
		
		#print speedCoeff
		#print mPos
	
	drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc,font)
	
	pygame.draw.rect(screen, (150,150,0), deadZone, 3)
	
	txt = font.render("FPS: "+str(1000/ms_elapsed), True, (0,150,150))
	screen.blit(txt, txtbound)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUNNING = False
	
	pygame.display.flip()
	
	ms_elapsed = pygame.time.get_ticks() - last_time
	
            
pygame.quit()
