# SPDX-License-Identifier: WTFPL

import glob
import csv
from pathlib import Path

things = {}

with open("original_mapname.csv", newline="", encoding="utf-8") as f:
    cr = csv.reader(f)
    for line in cr:
        if line[0] == "sha1":
            continue
        things[line[0]] = line[1]

for filename in glob.iglob("filelist/*.csv"):
    hash = Path(filename).stem
    if hash in things:
        continue
    with open(filename, newline='', encoding="utf-8") as f:
        cr = csv.reader(f)
        ain = ""
        matmaps = ""
        for line in cr:
            if line[0] == "filename":
                continue
            xd = Path(line[0])
            if xd.name == "cubemapdefault.vtf":
                b = Path(xd.parent).name
                things[hash] = b
                break
            if xd.suffix == ".ain":
                ain = xd.stem
            if matmaps == "" and line[0].startswith("materials/maps/"):
                matmaps = xd.parts[2]
        if not hash in things and ain != "":
            things[hash] = ain
        if not hash in things and matmaps != "":
            things[hash] = matmaps

with open("original_mapname.csv", "w", newline="", encoding="utf-8") as csvfile:
    mycsv = csv.writer(csvfile)
    mycsv.writerow(["sha1","mapname"])
    xxx = dict(sorted(things.items()))
    for k,v in xxx.items():
        mycsv.writerow([k, v])

#print(things)
