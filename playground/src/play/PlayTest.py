import unittest

class Test(unittest.TestCase):
    knownValues = ( ("some stuff", ["ddd"]),
                ("some other stuff", ["ddd"]))

    def testName(self):
        print "hiddf"
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()