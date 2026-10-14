# https://docs.python.org/3/library/unittest.html
"""
Unit tests for the binary search tree methods

"""

import unittest

from bst import *


class Test(unittest.TestCase):

    def test_remove(self):
        print(f"\nTests the method 'remove' in BST") 

        # Empty t = []
        t = [BST()]
        t[0].remove(6)
        self.assertEqual(str(t[0]),'<>')

        # Tree with single value [4]
        t[0].insert(4)
        t[0].remove(4)
        self.assertEqual(str(t[0]),'<>')

        
        def restoret():
            t[0] = BST()
            for x in [13, 8, 9, 6, 19, 15, 14, 18, 24, 3, 11]:
                t[0].insert(x)

        # Removal of leaf nodes
        restoret()
        t[0].remove(3)
        self.assertEqual(str(t[0]),'<6, 8, 9, 11, 13, 14, 15, 18, 19, 24>')
        t[0].remove(11)
        self.assertEqual(str(t[0]),'<6, 8, 9, 13, 14, 15, 18, 19, 24>')
        restoret()

        # Removal of nodes with empty left subtree 
        t[0].remove(9)
        self.assertEqual(str(t[0]),'<3, 6, 8, 11, 13, 14, 15, 18, 19, 24>')
        restoret()

        # Removal of nodes with empty right subtree 
        t[0].remove(6)
        self.assertEqual(str(t[0]),'<3, 8, 9, 11, 13, 14, 15, 18, 19, 24>')
        restoret()

        # Removal of nodes with two leaf children
        t[0].remove(15)
        self.assertEqual(str(t[0]),'<3, 6, 8, 9, 11, 13, 14, 18, 19, 24>')
        restoret()
        
        # Removal of nodes with two leaf children with children
        t[0].remove(19)
        self.assertEqual(str(t[0]),'<3, 6, 8, 9, 11, 13, 14, 15, 18, 24>')
        restoret()


if __name__ == "__main__":
    unittest.main()
