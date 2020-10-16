import sys
import csv
import numpy as np

from functools import reduce
from statistics import stdev, fmean
from collections import defaultdict

EXPECTED = 4
ANSWER = 1

TIMESTAMP = 0
ID = 1
DLC = 2
DATA = 3

def convert(filename):
    src = open(filename, 'r')
    rows = list(csv.reader(src))

    return rows[1:]

def distance(src, dst):
    src = int(src.replace(" ", ""), 16)
    dst = int(dst.replace(" ", ""), 16)
    return bin(src^dst).count('1')

def hamming(rows):
    cnt_max = [0 for _ in range(65)]
    cnt_min = [0 for _ in range(65)]
    cnt_avg = [0 for _ in range(65)]

    index = {}
    cur = 0
    memory = []
    progress = 1
    for row in rows:
        if ((progress % 10000) == 0):
            print(f'{progress/len(rows)}')
        progress += 1

        if row[ID] not in index:
            index[row[ID]] = cur
            cur += 1
            memory.append([row[DATA]])
        else:
            if row[5] == 'Normal':
                memory[index[row[ID]]].append(row[DATA])
            elif row[5] == 'Fuzzing' and len(memory[index[row[ID]]]) > 0:
                dists = list(map(lambda x: distance(x, row[DATA]), memory[index[row[ID]]]))
                dist_max = max(dists)
                dist_min = min(dists)
                cnt_max[dist_max] += 1
                cnt_min[dist_min] += 1
                cnt_avg[sum(dists)//len(dists)] += 1

    print(cnt_max)
    print(cnt_min)
    print(cnt_avg)
    return cnt_max

        
def save_hamming(rows):
    index = dict()
    cur = 0
    memory = []
    progress = 1
    for row in rows:
        if ((progress % 10000) == 0):
            print(f'{progress/len(rows)}')
        progress += 1

        if row[ID] not in index:
            index[row[ID]] = cur
            cur += 1
            memory.append([row[DATA]])
        else:
            if row[5] == 'Normal':
                memory[index[row[ID]]].append(row[DATA])

    #np.save("index.npy", index)
    np.save("memory.npy", np.array(memory))

        
        
if __name__ == "__main__":

    f1 = "Cybersecurity_Car_Hacking_D_training-2.csv"
    f2 = "ans_d_0.csv"
    
    rows = convert(f1)
    #answer = hamming(rows)
    save_hamming(rows)