#Do this for every unittest file#
import unittest
import xmlrunner
#-------------------------------#

from specialMath import findClosest

class testFindClosest(unittest.TestCase):
    """
    A test class for the findClosest module.
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        self.findClosest=findClosest
        self.worldSize = (10, 10)
        self.x1= (0,0)
		self.x2=(1,6)
		self.x3=(9,6)
        
    def tearDown(self):
        """
        clean up after any test
        tearDown is called after each test function execution.
        """

    def testHorizontal(self):
        self.assertEqual(self.findClosest(self.x1, self.x2, self.worldSize), (-2, 6))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(testFindClosest)
    xmlrunner.XMLTestRunner().run(suite)
