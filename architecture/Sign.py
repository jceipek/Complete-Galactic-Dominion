import pygame

"""

CREDITS FOR THIS MODULE: 

Christopher Night, Cambridge MA

Universe Factory games

Homepage

Email: Cosmologicon@gmail.com 

links - http://www.pygame.org/project-Panspermia-1126-.html
      - http://pyweek.org/u/Cosmologicon/

"""

class Fonts:
  fonts = {}
  def getfont(self, fname = None, fsize = 14):
    if not pygame.font.get_init(): pygame.font.init()
    spec = fname, fsize
    if spec in self.fonts: return self.fonts[spec]
    self.fonts[spec] = pygame.font.Font(fname, fsize)
    return self.fonts[spec]

class Sign:

  def __init__(self, sx, offset, image= None , imageSize= 50, centered = False, margin = 5, fname = None, fsize = 14):
    
    self.color0 = 150, 150, 150
    self.color1 = 180, 180, 180
    self.color2 = 100, 100, 100
    self.tcolor = 0, 0, 0

    self.image=image
    if self.image==None:
        self.imageSize=0
    else: self.imageSize=imageSize
    
    self.fname = fname
    self.fsize = fsize
    self.offset = offset
    self.font = Fonts().getfont(fname, fsize)
    self.sx, self.sy = sx, None
    self.tx=sx-self.imageSize
    self.surf = self.rect = None
    self.centered = centered
    self.text = []
    self.aa = True
    self.margin = margin
    self.rendered = False
    self.callback = lambda : 'It worked!'
  def clear(self):
    self.text = []
    self.rendered = False
  def addtext(self, text):
    for t in text.split("\n"):
      while t:
        r = len(t)
        while self.font.size(t[0:r-1])[0] + self.margin * 2 > self.tx:
          p = t.rfind(" ", 0, r-1)
          if p == -1: r -= 1
          else: r = p
        self.text.append(t[0:r])
        t = t[r:].strip()
    self.rendered = False
  def render(self):
    self.sy = len(self.text) * self.fsize + 2 * self.margin
    self.surf = pygame.Surface((self.sx, self.sy))
    self.rect = self.surf.get_rect()
    self.rect.topleft = self.offset
    self.surf.fill(self.color1)
    """
    for d in (0,1):
      w, h = self.sx-1-d, self.sy-1-d
      pygame.draw.line(self.surf, self.color0, (d,d), (d,h))
      pygame.draw.line(self.surf, self.color0, (d,d), (w,d))
      pygame.draw.line(self.surf, self.color2, (w,h), (d,h))
      pygame.draw.line(self.surf, self.color2, (w,h), (w,d))
    """
    y = self.margin
    for t in self.text:
      s = self.font.render(t, self.aa, self.tcolor)
      r = s.get_rect()
      if self.centered:
        r.midtop = (self.rect.centerx, y)
      else:
        r.topleft = (self.margin+self.imageSize, y)
      self.surf.blit(s, r)
      y += self.fsize
    if not self.image==None:
        thumb=pygame.transform.scale(self.image, (self.imageSize, self.imageSize))
        self.surf.blit(thumb, (self.margin, self.margin))
    self.rendered = True
  def draw(self, surf, f = 1):
    if not self.rendered: self.render()
    if f >= 1:
      surf.blit(self.surf, self.rect)
    else:
      s = pygame.Surface((int(self.sx * f), int(self.sy * f)))
      s.blit(self.surf, (0,0))
      surf.blit(s, self.rect)
