import glob
import csv
from pathlib import Path
import datetime
import os

things = {}

with open("timestamps.csv", newline="", encoding="utf-8") as f:
    cr = csv.reader(f)
    for line in cr:
        if line[0] == "sha1":
            continue
        things[line[0]] = line[1]

for filename in glob.iglob("../hashed/*.bsp"):
    hash = Path(filename).stem
    if not hash in things:
        things[hash] = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

with open("timestamps.csv", "w", newline="", encoding="utf-8") as csvfile:
    mycsv = csv.writer(csvfile)
    mycsv.writerow(["sha1","timestamp"])
    xxx = dict(sorted(things.items()))
    for k,v in xxx.items():
        mycsv.writerow([k, v])

#print(things)
