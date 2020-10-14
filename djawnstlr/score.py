import sys
import csv

EXPECTED = 4
ANSWER = 1

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

    return tp, fp, fn, tn


def get_f1(tp, fp, fn, tn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    f1 = 2 * (precision * recall) / (precision + recall)

    return f1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[-] Usage: python3 score.py problem.csv answer.csv")
    print(f"[*] Processing {sys.argv[2]} <= {sys.argv[1]}")
    tp, fp, fn, tn = score(sys.argv[1], sys.argv[2])
    print(f"[*] Processed.\ntp: {tp}\tfp: {fp}\nfn: {fn}\ttn: {tn}\n\nPrecision: {tp / (tp + fp) * 100}%\tRecall: {tp / (tp + fn) * 100}%\n")
    f1 = get_f1(tp, fp, fn, tn)
    print (f"F1-Score: {f1 * 100}")