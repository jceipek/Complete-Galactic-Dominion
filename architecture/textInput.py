# origins by Timothy Downs
# adjusted by Jared Kirschner

"""
Proof of concept for a textInput box.  Not implemented in CGD currently.
"""

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import thread,time

class textInput(object):
    
    def __init__(self,screen,question,fname=None,fsize=18,\
        screenOffset=(0,0),sx=200,sy=20,fontColor=(255,255,255),\
        backgroundColor=(0,0,0)):
        
        object.__init__(self)
        pygame.font.init()
        self.shiftDown = False
        self.screen = screen
        self.question = question
        self.message = []
        
        self.screenOffset = screenOffset
        
        self.sx = sx
        self.sy = sy
        #self.surface = pygame.Surface((self.sx,self.sy))
        #self.boundingRect = self.surface.get_rect()
        #self.boundingRect.topleft = self.screenOffset
        
        self.font = pygame.font.Font(fname,fsize)
        self.fontColor = fontColor
        self.backgroundColor = backgroundColor
        
        self.boundingRect = pygame.Rect(self.screenOffset,\
                                (self.sx,self.sy))
        
        self.lock = thread.allocate_lock()
        thread.start_new_thread(self.ask,())
        
    def getKey(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                return None

    def displayBox(self):
        pygame.draw.rect(self.screen,self.backgroundColor,self.boundingRect,0)
        textBox = self.boundingRect.inflate(-2,-2)
        
        pygame.draw.rect(self.screen,(255,255,255),textBox,1)
        
        if len(self.question) != 0:
            msg = self.makeMessage()
            self.screen.blit(self.font.render(msg,1,self.fontColor),\
                    self.boundingRect.inflate(-15,-10))
            pygame.display.flip()
    
    """
        self.rendered = False
    def render(self):
    self.sy = len(self.text) * self.fsize + 2 * self.margin
    self.surf = pygame.Surface((self.sx, self.sy))
    self.rect = self.surf.get_rect()
    self.rect.topleft = self.offset
    self.surf.fill(self.color1)
    for d in (0,1):
      w, h = self.sx-1-d, self.sy-1-d
      pygame.draw.line(self.surf, self.color0, (d,d), (d,h))
      pygame.draw.line(self.surf, self.color0, (d,d), (w,d))
      pygame.draw.line(self.surf, self.color2, (w,h), (d,h))
      pygame.draw.line(self.surf, self.color2, (w,h), (w,d))
    y = self.margin
    for t in self.text:
      s = self.font.render(t, self.aa, self.tcolor)
      r = s.get_rect()
      if self.centered:
        r.midtop = (self.rect.centerx, y)
      else:
        r.topleft = (self.margin, y)
      self.surf.blit(s, r)
      y += self.fsize
      """
    
    def makeMessage(self):
        return self.question + string.join(self.message,"")
    
    def ask(self):
        current_string = []
        self.displayBox()
        while 1:
            inkey = self.getKey()
            if inkey is not None:
                if inkey == K_BACKSPACE:
                    self.message = self.message[0:-1]
                    continue
                if inkey == 304:
                    self.shiftDown = True
                elif inkey == K_RETURN:
                    print string.join(self.message,"")
                    self.message = []
                elif 97 <= inkey <= 122:
                    if self.shiftDown:
                        inkey -= 32
                        self.shiftDown = False
                    self.message.append(chr(inkey))
                else:
                    try:
                        self.message.append(chr(inkey))
                    except ValueError:
                        pass
            self.displayBox()

def main():
    
    screen = pygame.display.set_mode((320,240))
    #thread.start_new_thread(myfunction,("Thread No:1",2,lock))
    #thread.start_new_thread(textInput,(screen,'Does it work',lock))
    tst = textInput(screen,'> ')
    timeTrack = 0
    sleepTime = 2
    while 1:
        timeTrack += sleepTime
        time.sleep(timeTrack)
        print timeTrack

if __name__ == '__main__': main()
