#!/usr/bin/env python3
""" MA3.py

Student: Olof Rörby
Mail: Ollerorby@hotmail.se
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from numba import njit

# Exc1
def approximate_pi(n, r = 1):
    # n is the number of points


    # Write your code here
    x_inside, y_inside = [], []
    x_outside, y_outside = [], []

    for _ in range (n):
         x = random.uniform(-r, r)
         y = random.uniform(-r, r)

         if x**2 + y**2 <= r:
              x_inside.append(x)
              y_inside.append(y)
         else: 
              x_outside.append(x)
              y_outside.append(y)

    plt.figure(figsize=(6, 6))
    plt.scatter(x_inside, y_inside, color='red', s=5)
    plt.scatter(x_outside, y_outside, color='blue', s=5)
    plt.xlim(-r, r)
    plt.ylim(-r, r)
    plt.gca().set_aspect('equal')
    plt.show()

    n_c = len(x_inside)
    pi_approx = 4 * n_c / n

    print(f'n = {n} gives the approximated pi = {pi_approx}')
    return pi_approx




# Exc2, approximation
def sphere_volume(n, d, r = 1): 
    # n is the number of points

    # d is the number of dimensions of the sphere 

    points = [[random.uniform(-r, r) for _ in range(d)] for _ in range(n)]

    inside_points = list(filter(
         lambda pt: sum(map(lambda x: x**2, pt)) <= r **2,
         points
    ))

    n_c = len(inside_points)
    return (n_c / n) * ((2 * r) ** d)

#Exc2, real value
def hypersphere_exact(n, d, r = 1):
    # n is the number of points

    # d is the number of dimensions of the sphere 

    return (m.pi ** (d / 2) / m.gamma((d / 2) + 1)) * (r ** d)

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int, r: float = 1.0)->float:
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
    
    n_c = 0
    r_sq = r*r

    for _ in range(n):
         sum_sq = 0.0
         for _ in range(d):
             x = random.uniform(-r, r)
             sum_sq += x * x
         if sum_sq <= r_sq:
             n_c +=1
         
    return (n_c / n) * ((2 * r) ** d)

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes

    n_per_process = n // np

    n_list = [n_per_process] * np
    d_list = [d] * np

    with future.ProcessPoolExecutor(max_workers=np) as executor:
         results = list(executor.map(sphere_volume, n_list, d_list))

    return mean(results)

    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    print("What is numba time?")

    ### run 1: 4.342626599999676
    ### run 2: 4.288382800000363
    ### run 3: 4.319270300000426

    ### numba run 1: 0.7045977000007042
    ### numba run 2: 0.633221400000366
    ### numba run 3: 0.6272741000002497
    ### much faster with numba, not the same pattern

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?") 

    for i in range(1, 4):
        start = pc()
        vol = sphere_volume_parallel(n, d)
        stop = pc()
        print(f"Parallel run {i}: {stop - start:.4f} seconds (volume: {vol:.4f})")

    ### run 1: 4.342626599999676
    ### run 2: 4.288382800000363
    ### run 3: 4.319270300000426

    ###my pc:

    ### Paralell run 1: 2.8625615000055404
    ### Paralell run 2: 2.8251995999889914
    ### Paralell run 3: 2.8469077999907313
    
    ###Linux server:


    ### Parallel run 1: 1.5116 seconds 
    ### Parallel run 2: 1.4744 seconds 
    ### Parallel run 3: 1.4776 seconds 
    

if __name__ == '__main__':
	main()
