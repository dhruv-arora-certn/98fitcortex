from multiprocessing import Pool
import random
import itertools

class F:
    def __init__(self):
        self.p = random.random()
        self.c = random.random()
        self.f = random.random()
        self.marked_diff = 0

def mark_diff(args):
    item = args[0]
    pi = args[1]
    item.marked_diff = (item.p/pi[0]+item.c/pi[1]+item.f/pi[2] - 3)**2
    return item

def mark(f_set , goal):
    with Pool(3) as p:
        data = p.map(mark_diff , zip(f_set , itertools.repeat(goal)))
    return data

if __name__ == "__main__":
    f_set = [F() for _ in range(10)]
    goal = [0.2,0.35,0.45]
    xs = mark(f_set, goal)
    for x in xs:
        print(x.marked_diff)