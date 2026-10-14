"""
Solutions to module 1
Student: Olof Rörby
E-mail: Olof.Rorby3502@student.uu.se
Reviewed by:
Review date:
"""

"""
Important notes: 
These examples are intended to practice RECURSIVE thinking. Thus, you may NOT 
use any loops nor built in functions like count, reverse, zip, math.pow etc. 

You may NOT use any global variables.

You can write code in the main function that demonstrates your solutions.
If you have test code running at the top level (i.e. outside the main function),
you have to remove it before uploading your code into Studium!
Also remove any trace and debugging printouts!

You may not import any packages other than time and math. These may
only be used in the analysis of the fib function.

In the oral presentation you must be prepared to explain your code and make minor 
modifications.

We have used type hints in the code below (see 
https://docs.python.org/3/library/typing.html).
Type hints serve as documentation and and don't affect the execution at all. 
If your Python doesn't allow type hints you should update to a more modern version!

"""




import time
import math

def multiply(m: int, n: int) -> int:  
    """Exc1: Computes m*n using additions"""
    if n == 0 or m == 0:
        return 0
    elif m > n:
        return m + multiply(m, n-1)
    else:
        return n + multiply(m-1, n)
    pass

def harmonic(n: int) -> float:              
    """Exc2: Computes and returns the harmonic sum 1 + 1/2 + 1/3 + ... + 1/n"""
    if n == 0:
        return print("Not real, division with 0")
    elif n == 1:
        return 1
    else:
       return (1/n + harmonic(n-1))
    pass


def get_binary(x: int) -> str:              
    """Exc3: Returns the binary representation of x"""
    if  x == 0:
        return "0"
    elif x == 1:
        return "1"
    elif x < 0:
        return "-" + get_binary(-x)
    else:
        return get_binary(x//2) + str(x%2)

    pass




def reverse_string(s: str) -> str:        
    """Exc4: Returns the string s reversed """
    if len(s) <=1:
        return s
    else:
        return s[-1]+reverse_string(s[:-1])
    pass


def largest(a: list):
    """Exc5: Returns the largest element in a"""
    if len(a) == 1:
        return a[0]
    max_of_rest = largest(a[1:])
    return a[0] if a[0] > max_of_rest else max_of_rest

    pass


def count(x, s: list) -> int:                
    """Exc6: Counts the number of occurences of x on all levels in s"""
    if len(s) == 0:
        return 0
    elif s[0] == x:
        return 1 + count(x, s[1:])
    elif type(s[0]) == list:
        return count(x, s[0]) + count(x, s[1:])
    else:
        return count(x, s[1:])

    pass

def bricklek(f: str, t: str, h: str, n: int) -> list[str]:
    """Exc7: Returns a list of string instructions for how to move the tiles"""
    if n == 0:
        return []
    else:
        return bricklek(f, h, t, n - 1) + [f'{f}->{t}'] + bricklek(h, t, f, n - 1)
    pass



def fib(n: int) -> int:                      
    """For Exc9: Returns the n:th Fibonacci number"""
    # You should verify that the time for this function grows approximately as
    # Theta(1.618^n) and also estimate how long time the call fib(100) would take.
    # The time estimate for fib(100) should be in reasonable units (most certainly
    # years) and, since it is just an estimate, with no more than two digits precision.
    #
    # Put your code at the end of the main function below!
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fib_mem(n):
    memory = {0:0, 1:1}

    def _fib_mem(n):
        if n not in memory:
            memory[n] = _fib_mem(n-1) + _fib_mem(n-2)
        return memory[n]
    
    return _fib_mem(n)

def main():
    print('\nCode that demonstrates my implementations\n')

    print('\n\nCode for analysing fib and fib_mem\n')
    #fib step
    """for n in range(35, 41):
        tstart = time.perf_counter()
        x = fib(n)
        tstop = time.perf_counter()
        print(f"n = {n}: fib({n}) = {x}, time = {(tstop - tstart):.2f} s")"""

    #fib_mem step
    n = 100
    tstart = time.perf_counter()
    x = fib_mem(n)
    tstop = time.perf_counter()
    print(f"n = {n}: fib({n}) = {x}, time = {(tstop - tstart)} s")


    print('\nBye!')


if __name__ == "__main__":
    main()

####################################################

"""
  Answers to the non-coding tasks
  ================================
  
  
  Exercise 8: Time for the tile game with 50 tiles:
  
  i tested all these
  print (len(bricklek('f','t','h', 1)))
    print (len(bricklek('f','t','h', 2)))
    print (len(bricklek('f','t','h', 3)))
    print (len(bricklek('f','t','h', 4)))
    print (len(bricklek('f','t','h', 5)))
    print (len(bricklek('f','t','h', 6)))
    to se the pattern and from what i could tell the formula is 2^(n)-1.
    so the answer to the question is 2^50-1 seconds wich is approx
    35702051 years

    ~35.7 million years
  
  Exercise 9: Time for Fibonacci:

  a)
  
  n has to be sufficiently large to prove that the algorithm grows by theta(1.618^n)
  thus I start the test at 35 and make 6 measurements that returns the time with 2 decimals.
  This will result in 5 ratios later!

  n = 35: fib(35) = 9227465, time = 1.80 s
  n = 36: fib(36) = 14930352, time = 2.67 s
  n = 37: fib(37) = 24157817, time = 4.29 s
  n = 38: fib(38) = 39088169, time = 6.97 s
  n = 39: fib(39) = 63245986, time = 11.36 s
  n = 40: fib(40) = 102334155, time = 18.24 s

  i notice now that maybe 35 was unnecessarily high starting point...
  however the ratio between all measured times are as follows:

  1: 1.48333...
  2: 1.60674....
  3: 1.62470...
  4: 1.62984...
  5: 1.60563...

  this is rather close to the target value 1.618 wich i believe is enough verification.
  the fluctuations i guess comes from rounding errors and perhaps not the exact same 
  computing power each time?

  b)

  The time fib(50) and fib(100) will take can be calculated by:
  t(50) = t(known) * 1.618^(50-known) and same for t(100)

  lets take the known time of fib(36) 2.67s 

  t(50) = 2.67 * 1.618^(14) = 2250.14499 s ~ 2250s ~ 42 min

  t(100) = 2.67 * 1.618^(64) = 6.326... * 10^13 s = 2.005994 * 10^6 years ~
  2.01 million years


  
  Exercise 10: Time for fib_mem:
  
  n = 100: fib(100) = 354224848179261915075, time = 3.309990279376507e-05 s
  
  
  Exercise 11: Comparison sorting methods:
  
  The time can be expressed as t(n) = c * f(n) where we take f(n) from O(f(n))
  thus the time for insertion sort can be expressed as t(n) = c * n^2 and for 
  merge sort as t(n) = c * n*log2(n).

  Given is t(1000) = 1 second for both methods =>
  insertion: c = t(n)/n^2 = 1/10^6 => c = 10^-6
  Merge: c = t(n)/(n*log2(n)) = 1/(1000*log2(1000)) => c = 1.00343 * 10^(-4) ~ 10~(-4)

  The time for n = 10^6:
    Insertion: t(10^6) = 10^(-6)* (10^(6))^2 = 10^6 seconds ~ 11.5 days
    Merge: t(10^6) = 10^(-4) * (10^(6) * log2(10^(6))) = 1999.99 ~ 2000 seconds ~ 33.33... minutes

    The time for n = 10^9
    Insertion: t(10^9) ~ 31 710 years
    Merge: t(10^9) ~ 35 days


  Exercise 12: Comparison Theta(n) and Theta(n log n)
  
  A solves a size n problem in n seconds

  B takes c*n*log_2(n) seconds to solve a size n problem. when n = 10 it takes 1 second to solve
  => 1 = c * 10 * log_2(10) => c = 1/(10*log(10)) = 0.03010299999 => c ~ 0.03
  plotting the functions of A and B shows that they intersect at n = 10^10

  so if n > 10^10 algorithm A is faster. 
"""
