#charged objects
from visual import *
from Gui import Callable
class Charge(object):
	"""Wrapper for charges"""
	def update(self):
		pass
	def makeMi(self):
		self.mi=self.panel.g.mi(self.panel.men, text=str(self), command=Callable(self.panel.select, self))
	def updateDrag(self):
		pass
		
class Point(Charge):
	"""
	represents point charge
	attributes: pos, charge, radius, color
	"""
	def __init__(self,pos=(0,0,0), charge=1, pan=None):
		self.pos=pos
		self.charge=charge

		self.s=sphere(pos=self.pos, radius=.001, color=(0,0,0))
		self.updateColor()
		self.panel=None
		
	def __str__(self):
		p=self.pos
		return '%dC point at (%d, %d, %d)' %(self.charge, p[0], p[1], p[2])
	def revert(self):
		self.s.color=self.color
	def updateDrag(self):
		self.pos=self.s.pos
	def updatePos(self,x,y,z):
		if len(x)<1: x=self.pos[0]
		if len(y)<1: y=self.pos[1]
		if len(z)<1: z=self.pos[2]
		self.pos=(int(x), int(y), int(z))
		self.s.pos=self.pos
		
	def updateCharge(self,c):
		self.charge=float(c)
		self.updateColor()
		
	def updateColor(self):
		self.radius=.1*abs(self.charge)**.5
		if self.charge> 0: self.color=(.1, .1, .9)
		elif self.charge< 0: self.color=(.9, .1, .1)
		else: self.color=(.9, .9, .1)
		self.s.radius=self.radius
		self.s.color=self.color
		
	

class Line(Charge):

	def __init__(self, eqn, density='.5', trange=[-5, 5], res=10):
		self.charge=density
		self.res=res
		
		self.t=t=arange(trange[0], trange[1], 1.0/self.res)

		self.lam=eval(self.charge+'+ 0*t')

		self.s=curve(x=0, y=0,z=0,red=0, green=0, blue=0, radius=.1)
		self.updatePos(*eqn)
		self.updateColor()
		self.panel=None
		
	def __str__(self):
		return '%s C/m line'%self.charge

	def revert(self):
		self.s.red=self.red
		self.s.green=self.green
		self.s.blue=self.blue
		
	def updatePos(self, x,y,z):
		self.pos=(x,y,z)
		t=self.t
		self.x=eval(self.pos[0])
		self.y=eval(self.pos[1])
		self.z=eval(self.pos[2])
		self.s.x=self.x
		self.s.y=self.y
		self.s.z=self.z
		
	def updateCharge(self,c):
		self.charge=c
		t=self.t
		self.lam=eval(self.charge+ '+ 0*t')
		self.updateColor()

	def updateColor(self):
		self.red=-1*self.lam
		self.green= 0
		self.blue=self.lam
		self.s.red=self.red
		self.s.green=self.green
		self.s.blue=self.blue
	
