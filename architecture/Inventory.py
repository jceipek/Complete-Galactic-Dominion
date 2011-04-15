class Inventory(object):
	"""
	Acts as an inventory for a Unit. Holds resources, items for use.
	"""

	def __init__(self):
		self.limit=100
		self.items={}
	def addToInventory(self, item, amount=1):
		self.items[item]=self.items.get(item,0)+amount

		
