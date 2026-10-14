""" bst.py

Student:
E-mail:
Reviewed by:
Date reviewed:
"""


from linked_list import LinkedList


class BST:

    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right

        def __iter__(self):     # Discussed in the text on generators
            if self.left:
                yield from self.left
            yield self.key
            if self.right:
                yield from self.right

    def __init__(self, root=None):
        self.root = root

    def __iter__(self):         # Discussed in the text on generators
        if self.root:
            yield from self.root

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, r, key):
        if r is None:
            return self.Node(key)
        elif key < r.key:
            r.left = self._insert(r.left, key)
        elif key > r.key:
            r.right = self._insert(r.right, key)
        else:
            pass  # Already there
        return r

    def print(self):
        self._print(self.root)

    def _print(self, r):
        if r:
            self._print(r.left)
            print(r.key, end=' ')
            self._print(r.right)

    """def contains(self, k): # given function
        n = self.root
        while n and n.key != k:
            if k < n.key:
                n = n.left
            else:
                n = n.right
        return n is not None """

    def contains(self, k): # Exc8: write recursive contains
        return self._contains(self.root, k)

    def _contains(self, r, k):
        if r is None:
             return False
        elif k == r.key:
            return True
        elif k < r.key:
            return self._contains(r.left, k)
        else:
            return self._contains(r.right, k)


    def size(self):
        return self._size(self.root)

    def _size(self, r):
        if r is None:
            return 0
        else:
            return 1 + self._size(r.left) + self._size(r.right)

#
#   Methods to be completed
#

    def height(self):             # Exc9     
        return self._height(self.root)
        pass

    def _height(self, r):
        if r is None:
            return 0
        else:
            return 1 + max(self._height(r.left), self._height(r.right))

    def __str__(self):            # Exc10
        return "<" + ", ".join(str(x) for x in self) + ">"       
        pass

    def to_list(self):            # Exc11   
        return list(self)
        pass
        # Complexity of to_list:
        # it is O(n) because it runs BST.__iter__ which only checks each node in the tree once

    def to_LinkedList(self):      # Exc12
        result = LinkedList()
        end = None

        for x in self:
            new_node = LinkedList.Node(x,None)
            if result.first is None:
                result.first = new_node
                end = result.first
            else:
                end.succ = new_node
                end = end.succ
        return result
        pass                      
        # Complexity of to_LinkedList:
        # This is O(n) because it uses the same type of method as in linked_list copy

    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, r, k):      # Exc13
        if r is None:
            return None
        elif k < r.key:
            r.left = self._remove(r.left, k)
            pass
            # r.left = left subtree with k removed
        elif k > r.key:
            r.right = self._remove(r.right, k)
            pass
            # r.right =  right subtree with k removed
        else:  # This is the key to be removed
            if r.left is None:     # Easy case
                return r.right
            elif r.right is None:  # Also easy case
                return r.left
            else:  # This is the tricky case.
                # Find the smallest key in the right subtree
                min_node = r.right
                while min_node.left:
                    min_node = min_node.left
                # Put that key in this node
                r.key = min_node.key
                # Remove that key from the right subtree
                r.right = self._remove(r.right, min_node.key)
                pass
        return r  # Remember this! It applies to some of the cases above



def main():
    t = BST()
    for x in [4, 1, 3, 6, 7, 1, 1, 5, 8]:
        t.insert(x)
    t.print()
    print()

    print('size  : ', t.size())
    for k in [0, 1, 2, 5, 9]:
        print(f"contains({k}): {t.contains(k)}")


if __name__ == "__main__":
    main()


"""
Exc14: In a binary search tree with n nodes and height h, what is the complexity in the
following scenarios:
==============================

1. Worst case of successful search
This should be O(h) as the worst case is a path from the root to a leaf which results in h steps
2. Worst case of unsuccessful search
Same here just that it finds None instead of the succesful key

"""
