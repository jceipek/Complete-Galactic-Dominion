import pygame

gridSize = 51
squareSize = 64

grid = dict()

for y in range(gridSize):
	for x in range(gridSize):
		if (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1):
			#checker black
			square = 0
		else:
			#checker white
			square = 1
		grid[(x,y)] = square

def drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc):
	#screenLoc is the absolute pixel location of the screen with respect to the
	#grid corners
	
	miny = (screenLoc[1]//squareSize)%gridSize
	maxy = ((screenLoc[1]+screenSize[1])//squareSize+1)%gridSize
	
	minx = (screenLoc[0]//squareSize)%gridSize
	maxx = ((screenLoc[0]+screenSize[0])//squareSize+1)%gridSize
	
	for y in range(miny,maxy):
		for x in range(minx,maxx):
			if grid[(x,y)] == 0:
				color = (0,0,0)
			else:
				color = (255,255,255)
			
			left = int(x*squareSize)
			top = int(y*squareSize)
			rect = pygame.Rect((left, top), (squareSize,squareSize))
			pygame.draw.rect(screen, color, rect)
			
			font = pygame.font.Font(pygame.font.get_default_font(), 16)
			txt = font.render(str((x,y)), True, (0,0,255))
			txtbound = txt.get_rect()
			txtbound.center = (left+squareSize/2,top+squareSize/2)
   			screen.blit(txt, txtbound)


screenSize = (width, height) = (640, 480)
RUNNING = True
pygame.init()
screen = pygame.display.set_mode(screenSize)
screenLoc = (64*3,64*3)

while RUNNING:
	screen.fill((255,0,0))
	
	drawVisible(screen,grid,gridSize,squareSize,screenSize,screenLoc)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUNNING = False
	
	pygame.display.flip()
            
pygame.quit()