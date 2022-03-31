from sudoku import Solver,Solver2
from GUI import Visualizer,getChar
import os, psutil;

import time
print("Select input: ", end='')
ip = input()
try:
    with open('input/'+ip+'.txt') as f:
        grid = []
        line = f.readline()
        while line:
            grid.append(list(map(lambda x:int(x) if x.isnumeric() else ord(x.upper())-ord('A')+10, line.split())))
            line = f.readline()
except:
    print('Can\'t open input file.')
    exit()


print('Select algorithm:')
print('\t1: Blind Search')
print('\t2: Heuristic')
alg = int(input())

if alg == 1:
    sudoku = Solver2(grid)
elif alg == 2:
    sudoku = Solver(grid)
else:
    print('Input invalid!')
    exit()

print('Demo step by step?')
print('\t1: Yes')
print('\t2: No')
demo = int(input())
if demo == 1:
    demo = True
elif demo == 2:
    demo = False
else:
    print('Input invalid!')
    exit()

ncount=0
if demo:
    vs=Visualizer(sudoku,grid)
    print('Press Space to go next step')
    print('Press Enter to auto next step')
    vs.run()
else:
    print('Solving...')
    tr = time.time()
    def func(x,y):
        global ncount
        ncount+=1

    result = sudoku.solve(0,func)

    tr = time.time() - tr
    if result:
        print('Solved!')
        for line in grid:
            print(' '.join(map(getChar,line))) 
    else:
        print('Can\'t solve this game :((')
        
    print("Time run:", tr,'seconds')
    print("Memory:",psutil.Process(os.getpid()).memory_info().rss,'bytes')
    print("Nodes count:", ncount)

