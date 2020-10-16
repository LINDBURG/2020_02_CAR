import sys
import csv

from functools import reduce
from statistics import stdev, fmean

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

def replay(rows):
    index = {}
    memory = []
    cur = 0
    progress = 1
    result = []
    for row in rows:
        if ((progress % 100000) == 0):
            print(f'{progress/len(rows)}')
        progress += 1

        line = row[ID] + row[DATA]
        if line not in index:
            index[line] = cur
            cur += 1
            # hash, last, avg, cnt, stdev, datas
            memory.append([line, float(row[TIMESTAMP]), 0, 1])
            result.append(True)
        elif memory[index[line]][3] == 1:
            memory[index[line]][2] = float(row[TIMESTAMP]) - memory[index[line]][1]
            memory[index[line]][1] = float(row[TIMESTAMP])
            memory[index[line]][3] += 1
            result.append(True)
        else:
            delta = float(row[TIMESTAMP]) - memory[index[line]][1]

            if delta < memory[index[line]][2] / 100:
                result.append(False)
            else:
                memory[index[line]][2] = (memory[index[line]][2]*memory[index[line]][3] + delta) / (memory[index[line]][3] + 1)
                memory[index[line]][1] = float(row[TIMESTAMP])
                memory[index[line]][3] += 1
                result.append(True)
    return result

def fuzzing(rows):
    index = {}
    cur = 0
    memory = []
    result = []
    progress = 1
    for row in rows:
        if ((progress % 100000) == 0):
            print(f'{progress/len(rows)}')
        progress += 1
        if row[ID] not in index:
            index[row[ID]] = cur
            cur += 1
            memory.append([row[DATA]])
            result.append(True)
        else:
            if len(memory[index[row[ID]]]) > 27:
                #위에 조건이 있으면 이유는 모르지만 빨라짐;;
                dists = list(map(lambda x: distance(x, row[DATA]), memory[index[row[ID]]]))
                #dist_max = max(dists)
                dist_min = min(dists)
                #avg = sum(dists)/len(dists)
                if dist_min > 25:
                    #print(len(dists))
                    result.append(False)
                else:
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
        answer.append([final,results[0][i], results[1][i], results[2][i], results[3][i]])
    return answer


def score(problem, answer):
    prob = open(problem, 'r')
    ans = open(answer, 'r')

    prob = list(csv.reader(prob))
    ans = list(csv.reader(ans))

    assert len(prob) == len(ans)

    tp, fp, fn, tn = 0, 0, 0, 0
    dfp = {'Flooding':0, 'Fuzzing':0, 'Replay':0, 'Spoofing':0, 'Normal':0}
    dfn = {'Flooding':0, 'Fuzzing':0, 'Replay':0, 'Spoofing':0, 'Normal':0}

    for idx in range(len(prob)):
        expected = prob[idx][EXPECTED]
        detected = ans[idx][ANSWER]
        sub = prob[idx][5]


        if expected == "Attack" and expected == detected:
            tp += 1
        elif expected == "Normal" and expected != detected:
            fp += 1
            if ans[idx][2] == 'False':
                dfp['Flooding'] += 1
            if ans[idx][3] == 'False':
                dfp['Spoofing'] += 1
            if ans[idx][4] == 'False':
                dfp['Fuzzing'] += 1
            if ans[idx][5] == 'False':
                dfp['Replay'] += 1
        elif expected == "Attack" and expected != detected:
            fn += 1
            dfn[sub] += 1
        elif expected == "Normal" and expected == detected:
            tn += 1
    print(tp, fp, fn, tn)
    print(dfp)
    print(dfn)
    return tp, fp, fn, tn


def get_f1(tp, fp, fn, tn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    f1 = 2 * (precision * recall) / (precision + recall)

    return f1
        
        
if __name__ == "__main__":

    f1 = "Cybersecurity_Car_Hacking_D_training-1.csv"
    f2 = "ans_d_0.csv"
    
    rows = convert(f1)
    answer = determine(rows, [flooding, spoofing, fuzzing, replay])

    dst = open(f2, "w", newline='')
    writer = csv.writer(dst)
    writer.writerow(['Number', 'Class'])
    for i in range(len(answer)):
        writer.writerow([str(i+1), 'Normal' if answer[i][0] else 'Attack', answer[i][1], answer[i][2], answer[i][3], answer[i][4]])

    dst.close()

    print("[*] Done.")
    #exit()

    print(f"[*] Processing {f2} <= {f1}")
    tp, fp, fn, tn = score(f1, f2)
    print(f"[*] Processed.\ntp: {tp}\tfp: {fp}\nfn: {fn}\ttn: {tn}\n\nPrecision: {tp / (tp + fp + 1) * 100}%\tRecall: {tp / (tp + fn + 1) * 100}%\n")
    f1 = get_f1(tp, fp, fn, tn)
    print (f"F1-Score: {f1 * 100}")