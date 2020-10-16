import sys
import csv

from functools import reduce
from statistics import stdev, fmean

EXPECTED = 4
ANSWER = 1

TIMESTAMP = 1
ID = 2
DLC = 3
DATA = 4

def convert(filename):
    src = open(filename, 'r')
    rows = list(csv.reader(src))

    return rows[1:]

def distance(src, dst):
    src = int(src.replace(" ", ""), 16)
    dst = int(dst.replace(" ", ""), 16)
    return bin(src^dst).count('1')

def replay(rows):
    index = {}
    memory = []
    cur = 0
    result = []
    for row in rows:
        hash = row[ID] + row[DATA]
        if hash not in index:
            index[hash] = cur
            cur += 1
            # hash, last, avg, cnt, stdev, datas
            memory.append([hash, float(row[TIMESTAMP]), 0, 1, 0, [float(row[TIMESTAMP])]])
            result.append(True)
        elif memory[index[hash]][3] == 1:
            memory[index[hash]][1] = float(row[TIMESTAMP])
            memory[index[hash]][2] = float(row[TIMESTAMP]) - memory[index[hash]][1]
            memory[index[hash]][3] = 2
            memory[index[hash]][5].append(float(row[TIMESTAMP]))
            memory[index[hash]][4] = stdev(memory[index[hash]][5])
            result.append(True)
        else:
            delta = float(row[TIMESTAMP]) - memory[index[hash]][1]
            if delta < memory[index[hash]][2] - memory[index[hash]][4]:
                result.append(False)
            else:
                memory[index[hash]][1] = float(row[TIMESTAMP])
                memory[index[hash]][2] = fmean(memory[index[hash]][5])
                memory[index[hash]][3] += 1
                memory[index[hash]][5].append(float(row[TIMESTAMP]))
                memory[index[hash]][4] = stdev(memory[index[hash]][5])
                result.append(True)
    return result

def fuzzing(rows):
    index = {}
    cur = 0
    memory = []
    result = []
    progress = 1
    for row in rows:
        if ((progress % 10000) == 0):
            print(f'{progress/len(rows)}')
        progress += 1
        if row[ID] not in index:
            index[row[ID]] = cur
            cur += 1
            memory.append([row[DATA]])
            result.append(True)
        else:
            if (row[DATA] not in memory) and len(memory[index[row[ID]]]) > 10:
                dists = list(map(lambda x: distance(x, row[DATA]), memory[index[row[ID]]]))
                dist = min(dists)
                if dist > 16:
                    result.append(False)
                else:
                    result.append(True)
                    #memory[index[row[ID]]].append(row[DATA])
            elif row[DATA] in memory:
                result.append(True)
            else:
                result.append(True)
                memory[index[row[ID]]].append(row[DATA])
    return result

def spoofing(rows):
    return list(map(lambda row: row[DATA] != "00 00 00 02 01 00 80 00" and row[DATA] != "28 E2 FF 28 25 00 01", rows))

def flooding(rows):
    return list(map(lambda row: int(row[ID], 16) != 0, rows))

def determine(rows, strategies):
    answer = []
    results = []
    for strategy in strategies:
        results.append(strategy(rows))
    for i in range(len(rows)):
        final = True
        for j in range(len(results)):
            final = final and results[j][i] 
        answer.append(final)
    return answer


def score(problem, answer):
    prob = open(problem, 'r')
    ans = open(answer, 'r')

    prob = list(csv.reader(prob))
    ans = list(csv.reader(ans))

    assert len(prob) == len(ans)

    tp, fp, fn, tn = 0, 0, 0, 0

    for idx in range(len(prob)):
        expected = prob[idx][EXPECTED]
        detected = ans[idx][ANSWER]


        if expected == "Attack" and expected == detected:
            tp += 1
        elif expected == "Normal" and expected != detected:
            fp += 1
        elif expected == "Attack" and expected != detected:
            fn += 1
        elif expected == "Normal" and expected == detected:
            tn += 1
    print(tp, fp, fn, tn)
    return tp, fp, fn, tn


def get_f1(tp, fp, fn, tn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    f1 = 2 * (precision * recall) / (precision + recall)

    return f1
        
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[-] Usage: python3 solve.py problem.csv answer.csv")
        exit()
    
    rows = convert(sys.argv[1])
    answer = determine(rows, [flooding, spoofing, fuzzing])

    dst = open(sys.argv[2], "w")
    writer = csv.writer(dst)
    writer.writerow(['Number', 'Class'])
    for i in range(len(answer)):
        writer.writerow([str(i+1), 'Normal' if answer[i] else 'Attack'])

    dst.close()

    print("[*] Done.")
    exit()

    print(f"[*] Processing {sys.argv[2]} <= {sys.argv[1]}")
    tp, fp, fn, tn = score(sys.argv[1], sys.argv[2])
    print(f"[*] Processed.\ntp: {tp}\tfp: {fp}\nfn: {fn}\ttn: {tn}\n\nPrecision: {tp / (tp + fp + 1) * 100}%\tRecall: {tp / (tp + fn + 1) * 100}%\n")
    f1 = get_f1(tp, fp, fn, tn)
    print (f"F1-Score: {f1 * 100}")