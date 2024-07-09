# SPDX-License-Identifier: WTFPL

import os
import glob
import bsp_tool # https://github.com/srcwr/bsp_tool
import gzip
import csv
from pathlib import Path

ignored = {}
with open("ignore.csv") as f:
    for line in f:
        stuff = line.split(",")
        ignored[stuff[0]] = stuff[1]

ignored_pak = ignored.copy()
with open("ignore_pak.csv") as f:
    for line in f:
        stuff = line.split(",")
        ignored_pak[stuff[0]] = stuff[1]

os.environ["EDITF"] = "ignore.csv"
for filename in glob.iglob("../hashed/*.bsp"):
    maphash = Path(filename).stem
    if maphash in ignored:
        continue
    newents = "entities/" + maphash + ".cfg"
    if os.path.exists(f"entitiesgz/{maphash}.cfg.gz"): # should read dir once & check the dict tbh... don't care... i'd rather leave this comment instead...
        continue
    print(maphash)
    os.environ["MAPHASH"] = maphash # used by my edits to bsp_tool to auto-add broken maps to ignore.csv...
    bsp = bsp_tool.load_bsp(filename)
    if "ENTITIES" in bsp.headers:
        ents = bsp.ENTITIES.as_bytes()[:-1] # -1 to remove trailing null byte
        with open(newents, "wb") as f:
            f.write(ents)
        with gzip.open(f"entitiesgz/{maphash}.cfg.gz", "wb") as f:
            f.write(ents)
    #break

os.environ["EDITF"] = "ignore_pak.csv"
for filename in glob.iglob("../hashed/*.bsp"):
    maphash = Path(filename).stem
    if maphash in ignored_pak and not ignored_pak[maphash].startswith("warning"):
        continue
    newents = "filelist/" + maphash + ".csv"
    if os.path.exists(newents): # should read dir once & check the dict tbh... don't care... i'd rather leave this comment instead...
        continue
    print(maphash)
    os.environ["MAPHASH"] = maphash # used by my edits to bsp_tool to auto-add broken maps to ignore_pak.csv...
    bsp = bsp_tool.load_bsp(filename)
    if "PAKFILE" in bsp.headers:
        try:
            files = bsp.PAKFILE.infolist()
        except:
            print("  error")
            with open("ignore_pak.csv", "a") as f:
                f.write(f"{maphash},error (no infolist)\n")
            continue
        #print(files)
        with open(newents, "w", newline="", encoding="utf-8") as csvfile:
            mycsv = csv.writer(csvfile)
            mycsv.writerow(["filename","size","compressed"])
            for x in files:
                mycsv.writerow([x.filename, x.file_size, x.compress_size])
