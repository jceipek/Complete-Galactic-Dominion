from random import randint
import threading
#import pygame
#from multiprocessing import Process, Pipe, Lock

#pygame.init()

def eventManager(events):
	print "Event Manager loop"
	for event in events:
		print event

def renderer():
   import pygame
   screenSize = (width, height) = (640, 480)
   pygame.init()
   screen = pygame.display.set_mode(screenSize)
   ms_elapsed = 0
   gameClock = pygame.time.Clock()
   while True:
       print "Renderer loop"
       
       print "starting Event manager"
       threading.Thread(target=eventManager,args=(pygame.event.get(),)).start()
       
       screen.fill((randint(0,255),0,0))
       pygame.display.flip()
       print ms_elapsed
       ms_elapsed = gameClock.tick()

if __name__ == '__main__':
   print "starting Renderer"
   a=threading.Thread(target=renderer)
   a.start()
   a.join()
