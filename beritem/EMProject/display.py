from threading import Thread
from time import sleep

from visual import *

from emmath import *
from charges import *

class Display(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.axes=[[-8, 8],[-8, 8],[-8, 8]]
		self.res =1.5
		self.pick=None
		self.drag_pos=None
		self.panel=None
		self.charges=[]
		self.change=False
		self.vfield={}
		self.vdots={}
		self.charges=[Point((3,3,3), 5), Point((-2,-2, -2), -20), Line(('t', 't', '-1*t')), Line(('t+1', '-1*t-2', '-1*t+3'), density='-.5')] #list of point charges
		scene.ambient=1
		scene.range=10
		
	def run(self):
		for c in self.charges:
			c.panel=self.panel
		#sets field of points
		field={}			
		for x in arange(*tuple(self.axes[0]+[self.res])):
			for y in arange(*tuple(self.axes[1]+[self.res])):
				for z in arange(*tuple(self.axes[2]+[self.res])):
					field[(x,y,z)]=0
		for p in field:
			self.vfield[p]=0
		for p in field:
			self.vdots[p]=sphere(pos=p, radius=.06, color=(1,1,1))

		
		
		drawAxes(self.axes)

		vrange= calcVoltage(self.vfield, self.charges)
		self.drawVolt(vrange)
		
		while 1:
			self.drag()
			if self.change: self.update()
			time.sleep(.1)
			
		pygame.quit()
		

	def update(self):
		for charge in self.charges:
			charge.updateDrag()
			charge.update()
		if self.change:
			vrange= calcVoltage(self.vfield, self.charges)
			self.drawVolt(vrange)
			#drawCharges(self.charges)
		self.change=False
						
	def drawVolt(self, vrange):
		"""
		draws voltage field
		"""
		maxv= max(abs(vrange[0]), abs(vrange[1]))
		if maxv==0:maxv=1
		for p in self.vdots:
			self.vdots[p].color=(-1*self.vfield[p]/maxv,0.03, (self.vfield[p]/maxv))

	def drag(self):
		if scene.mouse.events:
			m1 = scene.mouse.getevent() # obtain drag or drop event
			if m1.drag and m1.pick: # if clicked on the ball
				self.drag_pos = m1.pickpos # where on the ball the mouse was
				self.pick = m1.pick # pick is now True (nonzero)
			elif m1.drop: # released the mouse button at end of drag
				self.pick = None # end dragging (None is False)
		if self.pick:
			new_pos = scene.mouse.project(normal=(0,1,0)) # project onto xz plane
			if new_pos != self.drag_pos: # if the mouse has moved since last position
				self.pick.pos += new_pos - self.drag_pos # offset for where the ball was clicked
				self.drag_pos = new_pos # update drag position
				self.change=True
				
def drawAxes(axes):
	for i in range(3):
		minval=[0,0,0]
		maxval=[0,0,0]
		color=[.2,.2,.2]
		minval[i]=axes[i][0]
		maxval[i]=axes[i][1]
		color[i]=1
		color[(i+1)%3]=1
		curve(pos=[tuple(minval), tuple(maxval)], color=color)

def calcVoltage(vfield, charges):
	"""
	calculate voltage field
	"""
	minv=0
	maxv=0
	for p in vfield:
		vfield[p]=vAtPoint(p, charges)
		if vfield[p]>maxv: maxv=vfield[p]
		if vfield[p]<minv: minv=vfield[p]
	return [minv, maxv]

def calcEfield(efield, charges):
	for p in efield:
		efield[p]=eAtPoint(p, charges)





