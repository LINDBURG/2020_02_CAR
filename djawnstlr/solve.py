import sys
import csv

from functools import reduce

def convert(filename):
    src = open(filename, 'r')
    rows = list(csv.reader(src))

    return rows[1:]

def invalid_arbitration(rows):
    return list(map(lambda row: int(row[1], 16) == 0, rows))

def determine(rows, strategies):
    answer = []
    results = []
    for strategy in strategies:
        results.append(strategy(rows))
    for i in range(len(rows)):
        final = False
        for j in range(len(results)):
            final = (not final) and (not results[j][i]) 
        answer.append(not final)
    return answer
        
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[-] Usage: python3 solve.py problem.csv answer.csv")
        exit()
    
    rows = convert(sys.argv[1])
    answer = determine(rows, [invalid_arbitration])

    dst = open(sys.argv[2], "w")
    writer = csv.writer(dst)
    writer.writerow(['lineno', 'result'])
    for i in range(len(answer)):
        writer.writerow([str(i), 'Attack' if answer[i] else 'Normal'])

    dst.close()