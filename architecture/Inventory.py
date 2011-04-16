class Inventory(object):
	"""
	Acts as an inventory for a Unit. Holds resources, items for use.
	"""

	def __init__(self):
		self.limit=100
		self.items={}
		
	def __str__(self):
		s='Inventory: \n'
		for item in self.items:
			s+= item +' : ' + str(self.items[item])+ '\n'
		if not self.items:
			s+='No items'
		return s
		
	def addToInventory(self, item, amount=1):
		self.items[item]=self.items.get(item,0)+amount
		

		
