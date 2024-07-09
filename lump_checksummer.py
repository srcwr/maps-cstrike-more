# SPDX-License-Identifier: WTFPL

import glob
import bsp_tool # https://github.com/srcwr/bsp_tool
import csv
from pathlib import Path
import hashlib

print("finding ignored...")
ignored = {}
with open("ignore.csv") as f:
    for line in f:
        stuff = line.split(",")
        ignored[stuff[0]] = stuff[1]

print("finding existing...")
lump_checksums = {}
with open("lump_checksums.csv", newline="", encoding="utf-8") as f:
    cr = csv.reader(f)
    for line in cr:
        if line[0] == "sha1":
            continue
        lump_checksums[line[0]] = line[1]

print("finding first map or something...")
for filename in glob.iglob("../hashed/*.bsp"):
    maphash = Path(filename).stem
    if maphash in ignored or maphash in lump_checksums:
        continue
    print(maphash)
    bsp = bsp_tool.load_bsp(filename)
    f = open(filename, "rb")
    h = hashlib.md5(usedforsecurity=False)
    for k,v in bsp.headers.items():
        if k == "ENTITIES":
            continue
        f.seek(v.offset)
        l = f.read(v.length)
        h.update(l)
    f.close()

    lump_checksums[maphash] = h.hexdigest()
    print("   ", h.hexdigest())

with open("lump_checksums.csv", "w", newline="", encoding="utf-8") as csvfile:
    mycsv = csv.writer(csvfile)
    mycsv.writerow(["sha1","lump_md5_checksum"])
    xxx = dict(sorted(lump_checksums.items()))
    for k,v in xxx.items():
        mycsv.writerow([k, v])
