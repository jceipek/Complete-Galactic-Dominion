class Event(object):
	
	def __init__(self):
		object.__init__(self)

class StartEvent(Event):
	
	def __init__(self):
		from datetime import datetime
		object.__init__(self)
		self.timestamp = datetime.today()
