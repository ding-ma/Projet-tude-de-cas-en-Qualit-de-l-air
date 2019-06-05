import csv

with open("Book1.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        print ('line[{}] = {}'.format(i, line))
        print(line[0])