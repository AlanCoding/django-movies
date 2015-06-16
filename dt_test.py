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
        dt = datetime.datetime.fromtimestamp(int(row[3]) )
        print("   "+str(i))
        print(dt)
        print(dt.isoformat())
        print(repr(dt))
        if i > 10:
            break

print(" ")
dt = datetime.datetime.fromtimestamp(978229409)
print(dt)
print(datetime.datetime(2000, 7, 14, 12, 30))
print((dt - datetime.datetime(1970, 1, 1)).total_seconds())

print(" ")
print(datetime.datetime.now())
