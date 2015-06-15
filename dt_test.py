import csv
import datetime

source_base = "../data/ml-1m/"

print("Converting ratings...")
ratings = []
with open(source_base + "ratings.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    i = 0
    for row in reader:
        i += 1
        print(row[3])
        print(datetime.datetime.fromtimestamp(int(row[3]) ))
        if i > 10:
            break

print(datetime.datetime(2000, 7, 14, 12, 30))
