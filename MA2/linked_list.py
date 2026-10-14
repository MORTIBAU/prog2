""" linked_list.py

Student:
Mail:
Reviewed by:
Review date:
"""
class Person: #for Ex7
    def __init__(self, name, pnr):
        self.name = name
        self.pnr = pnr

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'{self.name}:{self.pnr}'

    


class LinkedList:

    class Node:
        def __init__(self, data, succ):
            self.data = data
            self.succ = succ

    def __init__(self):
        self.first = None

    def __iter__(self):            # Discussed in the section on iterators and generators
        current = self.first
        while current:
            yield current.data
            current = current.succ

    def __contains__(self, x):           # Discussed in the section on operator overloading
        for d in self:
            if d == x:
                return True
            elif x < d:
                return False
        return False

    def insert(self, x):
        if self.first is None or x <= self.first.data:
            self.first = self.Node(x, self.first)
        else:
            f = self.first
            while f.succ and x > f.succ.data:
                f = f.succ
            f.succ = self.Node(x, f.succ)

    def print(self):
        print('(', end='')
        f = self.first
        while f:
            print(f.data, end='')
            f = f.succ
            if f:
                print(', ', end='')
        print(')')

    # To be implemented

    def length(self):             # Exc1
        count = 0
        f = self.first
        while f:
            count += 1
            f = f.succ
        return count
        pass

    def remove_last(self):        # Exc2
        if self.first is None:
            raise ValueError('Empty list')
        elif self.first.succ is None:
            data = self.first.data
            self.first = None
            return data

        f = self.first
        while f.succ.succ is not None:
            f = f.succ
            
        data = f.succ.data
        f.succ = None
        return data
        pass

    def remove(self, x):          # Exc3
        if self.first is None:
            return False

        elif self.first.data == x:
            self.first = self.first.succ
            return True

        else:
            f = self.first
            while f.succ is not None:
                if f.succ.data == x:
                    f.succ = f.succ.succ
                    return True
                f = f.succ

        return False

        pass

    def to_list(self):            # Exc4
        def _to_list(f):
            if f is None:
                return []
            else:
                return [f.data] + _to_list(f.succ)
        return _to_list(self.first)
        pass

    def __str__(self):            # Exc5
        return "(" + ", ".join(str(x) for x in self) + ")"
        pass

    """ def copy(self):
        result = LinkedList()
        for x in self:
            result.insert(x)
        return result
        # Complexity for this implementation: 
        # O(n^2) since result.insert(x) takes O(k) operations, where k is the length of result, and the loop makes it iterate n times for all elements in self => n*n
        pass """


    def copy(self):               # Exc6, should be more efficient
        Result = LinkedList()
        if self.first is None:
            return Result

        Result.first = LinkedList.Node(self.first.data, None)
        end = Result.first
        current = self.first.succ
        
        while current:
            end.succ = LinkedList.Node(current.data, None)
            end = end.succ
            current = current.succ

        return Result
    
        pass                      
    ##    # Complexity for this implementation:
    ##    # The complexity here is O(n) because the end node always point to the last one where the new node should be added, thus resulting in O(1) for each single copy => O(n) for the total of elements n



def main():
    lst = LinkedList()
    for x in [1, 1, 1, 2, 3, 3, 2, 1, 9, 7]:
        lst.insert(x)
    lst.print()

    # Test code:

    plst = LinkedList()
    p = Person('Olle', '7771')
    plst.insert(p)
    plst.print()

    q = Person('Joel', '6767')
    plst.insert(q)
    print(plst)






if __name__ == '__main__':
    main()
