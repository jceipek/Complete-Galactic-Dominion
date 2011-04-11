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
        self.x1=(1,9)
        self.x2=(9,9)
        self.x3=(1,1)
        self.x4=(9,1)
        self.x5=(5,5)
        
    def tearDown(self):
        """
        clean up after any test
        tearDown is called after each test function execution.
        """

    def testHorizontal(self):
        self.assertEqual(self.findClosest(self.x1, self.x2, self.worldSize), (-1, 9))

    def testVertical(self):
        self.assertEqual(self.findClosest(self.x2, self.x4, self.worldSize), (9,11))

    def testDiagonal(self):
        self.assertEqual(self.findClosest(self.x2, self.x3, self.worldSize), (11,11))

    def testOtherDiag(self):
        self.assertEqual(self.findClosest(self.x4, self.x1, self.worldSize), (11,-1))

    def testSameGrid(self):
        self.assertEqual(self.findClosest(self.x2, self.x5, self.worldSize), (5,5))

    


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(testFindClosest)
    xmlrunner.XMLTestRunner().run(suite)
