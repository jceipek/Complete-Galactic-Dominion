import Builder
class Structure(Builder)
"""Defines structues which are built by units"""
	timeToBuild=0 #first definition of timeToBuild
	resourcesRequired=None #first definition of resourcesRequired
	def __init__(self):
		Builder.__init__(self)
		
