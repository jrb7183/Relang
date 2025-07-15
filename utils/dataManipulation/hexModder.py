import csv
import sys

with open("../data/data.txt", "r") as f:
    lines = f.readlines()

data_rows = []
i = 0

bit3 = sys.argv[1]
bit4 = sys.argv[2]

for line in lines:
    if line[2] not in ["4", "5", "6", "7", "C", "D", "E", "F"]:
        
        if line[2] == '0' or line[2] == '1':
            i = 0

        if i < len(data_rows):
            data_rows[i] += ["'" + bit4 + bit3 + line[2:-1]]
        else:
            data_rows += [["'" + bit4 + bit3 + line[2:-1]]]
        
        i += 1


out = open("../data/output.csv", "w", newline='')
writer = csv.writer(out)
for row in data_rows:
    print(row)
    writer.writerow(row)
        
out.close()