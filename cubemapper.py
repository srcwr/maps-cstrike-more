import glob
import csv
from pathlib import Path

things = {}

for filename in glob.iglob("filelist/*.csv"):
    with open(filename, newline='', encoding="utf-8") as f:
        cr = csv.reader(f)
        for line in cr:
            if line[0] == "filename":
                continue
            if Path(line[0]).name == "cubemapdefault.vtf":
                a = Path(filename).stem
                b = Path(Path(line[0]).parent).name
                things[a] = b
                break

with open("original_mapname.csv", "w", newline="", encoding="utf-8") as csvfile:
    mycsv = csv.writer(csvfile)
    mycsv.writerow(["sha1","mapname"])
    xxx = dict(sorted(things.items()))
    for k,v in xxx.items():
        mycsv.writerow([k, v])

print(things)
