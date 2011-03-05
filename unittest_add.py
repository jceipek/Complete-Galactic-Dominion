#Do this for every unittest file#
import unittest
import xmlrunner
#-------------------------------#

import add

class testAdd(unittest.TestCase):
    """
    A test class for the add module.
    """

    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        self.add = add.add
        self.num1 = 5
        self.num2 = 11.4
        self.num3 = -4
        
    def tearDown(self):
        """
        clean up after any test
        tearDown is called after each test function execution.
        """

    def testAddInts(self):
        self.assertEqual(self.add(self.num1,self.num1), 11)#10)

    def testAddFloats(self):
        self.assertEqual(self.add(self.num2,self.num2), 22.8)
        
    def testAddIntToFloat(self):
        self.assertEqual(self.add(self.num1,self.num2), 16.4)
        
    def testAddNegInts(self):
        self.assertEqual(self.add(self.num3,self.num3), -8)
        
    def testAddPosNegInts(self):
        self.assertEqual(self.add(self.num1,self.num3), 50)#1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(testAdd)
    xmlrunner.XMLTestRunner().run(suite)
