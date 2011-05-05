#control panel
from threading import Thread
from visual.controls import *
from time import sleep
from charges import *

class Panel(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.field=None
		self.activeCharge=None

	def run(self):
		
		def change(x): # Called by controls when button is clicked
			if b.text == 'Click me':
				b.text = 'Try again'
				self.addPoint([3,-1,3], 40)
			else:
				b.text = 'Click me'
			print 'change called'
		
		def changeMenu(ch):
			m.text='Hello'
			if self.activeCharge:
				self.activeCharge.revert()
			self.select(ch)
			print 'I done got called'

		def g(x):
			return lambda: changeMenu(x)
			
			
 		c = controls(x=500, y=50, width=500, height=200, range=250) # Create controls window
		# Create a button in the controls window:
		b = button( pos=(0,0), width=150, height=30, text='Click me', action=lambda: change(0) )

		
		m=menu(text='Select Charge', pos=(-100, 50), width=200, height=15)

		
		for i in range(len(self.field.charges)):
			text=str(self.field.charges[i])
			m.items.append((text, g(self.field.charges[i])))		

		self.field.start()
		scene.range=10
		pick=None
		while 1:
			c.interact() # Check for mouse events and drive specified actions
			if scene.mouse.events:
				m1 = scene.mouse.getevent() # obtain drag or drop event
				if m1.drag and m1.pick: # if clicked on the ball
					drag_pos = m1.pickpos # where on the ball the mouse was
					pick = m1.pick # pick is now True (nonzero)
				elif m1.drop: # released the mouse button at end of drag
					pick = None # end dragging (None is False)
			if pick:
				new_pos = scene.mouse.project(normal=(0,1,0)) # project onto xz plane
				if new_pos != drag_pos: # if the mouse has moved since last position
					pick.pos += new_pos - drag_pos # offset for where the ball was clicked
					drag_pos = new_pos # update drag position
					self.field.change=True
					
			time.sleep(.005)

		pygame.quit()

	def addPoint(self,pos, q=1):
		self.field.charges.append(Point(pos, q))
		self.field.change=True
	def select(self, charge):
			self.activeCharge=charge
			charge.s.color=(1,1,1)
		


