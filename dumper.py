# SPDX-License-Identifier: WTFPL

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "bsp_tool @ git+https://github.com/srcwr/bsp_tool@dc486011ab5bfee6f68f32367c1127e8b972b3a5",
# ]
# ///

import os
import glob
import bsp_tool # https://github.com/srcwr/bsp_tool
import gzip
import csv
import re
from pathlib import Path

vscript_filelist_probably = set()
vscript_entities_probably = set()

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
        if re.search(b"(script |script_execute|RunScriptCode|RunScriptFile|CallScriptFunction)", ents, re.I):
            vscript_entities_probably.add(maphash)
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
                if ("vscripts" in x.filename.lower()) or x.lower().endswith(".nut"):
                    vscript_filelist_probably.add(maphash)
                mycsv.writerow([x.filename, x.file_size, x.compress_size])


if len(vscript_filelist_probably) > 0 or len(vscript_entities_probably) > 0:
    print("vscript probably exists, so doing csv stuff")
    vscript_csv = {}
    with open("vscript_probably.csv", newline="", encoding="utf-8") as f:
        cr = csv.reader(f)
        for line in cr:
            if line[0] == "sha1":
                continue
            vscript_csv[line[0]] = line[1]
    for maphash in (vscript_filelist_probably&vscript_entities_probably):
        vscript_csv[maphash] = "filelist & entities"
    for maphash in (vscript_filelist_probably-vscript_entities_probably):
        vscript_csv[maphash] = "filelist"
    for maphash in (vscript_entities_probably-vscript_filelist_probably):
        vscript_csv[maphash] = "entities"

    with open("vscript_probably.csv", "w", newline="", encoding="utf-8") as csvfile:
        mycsv = csv.writer(csvfile)
        mycsv.writerow(["sha1","reason"])
        xxx = dict(sorted(vscript_csv.items()))
        for k,v in xxx.items():
            mycsv.writerow([k, v])
