import sys
import csv

def convert(filename):
    src = open(filename, 'r')
    rows = list(csv.reader(src))

    return rows[1:]

        
if __name__ == "__main__":

    f1 = []
    f1.append("Cybersecurity_Car_Hacking_D_training-1.csv")
    f1.append("Cybersecurity_Car_Hacking_D_training-2.csv")
    f1.append("Cybersecurity_Car_Hacking_S_training-1.csv")
    f1.append("Cybersecurity_Car_Hacking_S_training-2.csv")
    f2 = "Cybersecurity_Car_Hacking_A_training-1.csv"
    
    dst = open(f2, "w", newline='')
    writer = csv.writer(dst)
    writer.writerow(['Timestamp','Arbitration_ID','DLC','Data','Class', 'SubClass'])
    for f in f1:
        rows = convert(f)
        print(f)
        for row in rows:
            writer.writerow(row)

    dst.close()