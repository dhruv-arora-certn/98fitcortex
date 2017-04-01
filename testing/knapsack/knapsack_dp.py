#!/usr/bin/env python3

import sys

def knapsack(food_list, limit):
    """straightforward DP solution
    
    Arguments:
    - `v`: list of values
    - `w`: list of weights
    - `limit`: maximum limit
    - `n`: number of items
    """
    n = len(food_list)
    limit = round(limit)
    F = [[0] * (limit + 1) for x in range(n + 1)]
    test = []
    for i in range(0, n):                # F[-1] is all 0.
        for j in range(limit + 1):
            if j >= food_list[i].calorie:
                l = max(F[i - 1][j], F[i - 1][j - food_list[i].calorie] + round(1/food_list[i].squared_diff))
                test.append(l)
                F[i][j] = l
            else:
                F[i][j] = F[i - 1][j]
    return F , test

def display(F , limit , food_list):
    y  = round(limit)
    n = len(F)
    items = []
    for i in range(n - 1, -1, -1):
        if F[i][y] > F[i - 1][y]:
            items.append(i)
            y -= round(food_list[i].calorie)
    return items

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        sys.exit(1)

    with open(filename) as f:
        limit, n = map(int, f.readline().split())
        v, w = zip(*[map(int, ln.split()) for ln in f.readlines()])

    F = knapsack(v, w, limit, n)
    print("Max value:", F[n - 1][limit])
        
    """ Display selected items"""
    y = limit
    for i in range(n - 1, -1, -1):
        if F[i][y] > F[i - 1][y]:
            print ("item: ", i, "value:", v[i], "weight:", w[i])
            y -= w[i]
