class Inventory(object):
	"""
	Acts as an inventory for a Unit. Holds resources, items for use.
	"""
	
	def __init__(self):
		object.__init__(self)
		
		self.limit = 100
		
		# Dictionary mapping classes to amounts
		self.items = {}
		self.itemCount = 0		

	def __str__(self):
		s='Inventory: \n'
		for item in self.items:
			s+= item +' : ' + str(self.items[item])+ '\n'
		if not self.items:
			s+='No items'
		return s		
		
	def add(self,item,amount=1):
		"""
		Takes an object reference (item), and adds the given amount
		of it to the inventory.  As much as can be added will be, and
		the amount added will be returned.
		"""
		
		if self.isFull(): return 0
		
		itemClass = item.__class__
		if (self.itemCount + amount) <= self.limit:
			self.items[itemClass]=self.items.get(itemClass,0)+amount
			self.itemCount += amount
			return amount
		else:
			space = self.limit - self.itemCount
			self.items[itemClass]=self.items.get(itemClass,0)+space
			self.itemCount+=space
			return space

	def isFull(self):
		return self.itemCount >= self.limit
		
	def getItemCount(self):
		return self.itemCount
	
	def recalculateItemCount(self):
		return sum(self.items.values())
